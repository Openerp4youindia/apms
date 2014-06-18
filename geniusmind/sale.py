
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################


import time
from openerp.osv import fields, osv
from openerp.tools.translate import _

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc


class sale_order(osv.osv):
    _inherit = 'sale.order'
    _columns = {
            'printed_note': fields.text('Printed Notes'),
            'pur_number':fields.char('Purchase Order/Number',size=64),
            'pur_date':fields.date('Purchase Order/date'),
        }

#    def action_wait(self, cr, uid, ids, context=None):
#        for o in self.browse(cr, uid, ids):
#            if not o.order_line:
#                raise osv.except_osv(_('Error !'),_('You cannot confirm a sale order which has no line.'))
#            if (o.order_policy == 'manual'):
#                if not o.name:
#                    name = self.pool.get('ir.sequence').get(cr, uid, 'sale.order')
#                self.write(cr, uid, [o.id], {'state': 'manual', 'name':o.name or name,'date_confirm': fields.date.context_today(self, cr, uid, context=context)})
#            else:
#                if not o.name:
#                    name = self.pool.get('ir.sequence').get(cr, uid, 'sale.order')
#                self.write(cr, uid, [o.id], {'state': 'progress','name':o.name or name, 'date_confirm': fields.date.context_today(self, cr, uid, context=context)})
#            self.pool.get('sale.order.line').button_confirm(cr, uid, [x.id for x in o.order_line])
#            
#            message = _("The quotation '%s' has been converted to a sales order.") % (o.name or name,)
#            self.log(cr, uid, o.id, message)
#        return True
    
    def _make_invoice(self, cr, uid, order, lines, context=None):
        journal_obj = self.pool.get('account.journal')
        inv_obj = self.pool.get('account.invoice')
        obj_invoice_line = self.pool.get('account.invoice.line')
        if context is None:
            context = {}

        journal_ids = journal_obj.search(cr, uid, [('type', '=', 'sale'), ('company_id', '=', order.company_id.id)], limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error !'),
                _('There is no sales journal defined for this company: "%s" (id:%d)') % (order.company_id.name, order.company_id.id))
        a = order.partner_id.property_account_receivable.id
        pay_term = order.payment_term and order.payment_term.id or False
        invoiced_sale_line_ids = self.pool.get('sale.order.line').search(cr, uid, [('order_id', '=', order.id), ('invoiced', '=', True)], context=context)
        from_line_invoice_ids = []
        for invoiced_sale_line_id in self.pool.get('sale.order.line').browse(cr, uid, invoiced_sale_line_ids, context=context):
            for invoice_line_id in invoiced_sale_line_id.invoice_lines:
                if invoice_line_id.invoice_id.id not in from_line_invoice_ids:
                    from_line_invoice_ids.append(invoice_line_id.invoice_id.id)
        for preinv in order.invoice_ids:
            if preinv.state not in ('cancel',) and preinv.id not in from_line_invoice_ids:
                for preline in preinv.invoice_line:
                    inv_line_id = obj_invoice_line.copy(cr, uid, preline.id, {'invoice_id': False, 'price_unit': -preline.price_unit})
                    lines.append(inv_line_id)
        inv = {
            'name': order.client_order_ref or '',
            'origin': order.name,
            'type': 'out_invoice',
            'reference': order.client_order_ref or order.name,
            'account_id': a,
            'partner_id': order.partner_id.id,
            'journal_id': journal_ids[0],
            'address_invoice_id': order.partner_invoice_id.id,
#            'address_contact_id': order.partner_order_id.id,
            'invoice_line': [(6, 0, lines)],
            'currency_id': order.pricelist_id.currency_id.id,
            'comment': order.note,
            'payment_term': pay_term,
            'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
            'date_invoice': context.get('date_invoice',False),
            'company_id': order.company_id.id,
            'user_id': order.user_id and order.user_id.id or False,
            'printed_note': order.printed_note or '',
            'pur_number': order.pur_number or '',
            'pur_date':order.pur_date or False,
#            'address_shipping_id':order.partner_shipping_id.id,
	         'sale_id':order.id,
        }
        inv.update(self._inv_get(cr, uid, order))
        inv_id = inv_obj.create(cr, uid, inv, context=context)
        data = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], pay_term, time.strftime('%Y-%m-%d'))
        if data.get('value', False):
            inv_obj.write(cr, uid, [inv_id], data['value'], context=context)
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id

    def manual_invoice(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        wf_service = netsvc.LocalService("workflow")
        inv_ids = set()
        inv_ids1 = set()
        for id in ids:
            for record in self.pool.get('sale.order').browse(cr, uid, id).invoice_ids:
                inv_ids.add(record.id)
        # inv_ids would have old invoices if any
        for id in ids:
            wf_service.trg_validate(uid, 'sale.order', id, 'manual_invoice', cr)
            for record in self.pool.get('sale.order').browse(cr, uid, id).invoice_ids:
                inv_ids1.add(record.id)
        inv_ids = list(inv_ids1.difference(inv_ids))

        res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
        res_id = res and res[1] or False,

        return {
            'name': 'Customer Invoices',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': 'account.invoice',
            'context': "{'type':'out_invoice','journal_type': 'sale'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': inv_ids and inv_ids[0] or False,
        }

    def action_invoice_create(self, cr, uid, ids, grouped=False, states=['confirmed', 'done', 'exception'], date_inv = False, context=None):
        res = False
        invoices = {}
        invoice_ids = []
        picking_obj = self.pool.get('stock.picking')
        invoice = self.pool.get('account.invoice')
        obj_sale_order_line = self.pool.get('sale.order.line')
        if context is None:
            context = {}
        # If date was specified, use it as date invoiced, usefull when invoices are generated this month and put the
        # last day of the last month as invoice date
        if date_inv:
            context['date_inv'] = date_inv
        for o in self.browse(cr, uid, ids, context=context):
            lines = []
            for line in o.order_line:
                if line.invoiced:
                    continue
                elif (line.state in states):
                    lines.append(line.id)
            created_lines = obj_sale_order_line.invoice_line_create(cr, uid, lines)
            if created_lines:
                invoices.setdefault(o.partner_id.id, []).append((o, created_lines))
        if not invoices:
            for o in self.browse(cr, uid, ids, context=context):
                for i in o.invoice_ids:
                    if i.state == 'draft':
                        return i.id
        for val in invoices.values():
            if grouped:
                res = self._make_invoice(cr, uid, val[0][0], reduce(lambda x, y: x + y, [l for o, l in val], []), context=context)
                invoice_ref = ''
                for o, l in val:
                    invoice_ref += o.name + '|'
                    self.write(cr, uid, [o.id], {'state': 'progress'})
                    if o.order_policy == 'picking':
                        picking_obj.write(cr, uid, map(lambda x: x.id, o.picking_ids), {'invoice_state': 'invoiced'})
                    cr.execute('insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)', (o.id, res))
                invoice.write(cr, uid, [res], {'origin': invoice_ref, 'name': invoice_ref})
            else:
                for order, il in val:
                    res = self._make_invoice(cr, uid, order, il, context=context)
                    invoice_ids.append(res)
                    self.write(cr, uid, [order.id], {'state': 'progress'})
                    if order.order_policy == 'picking':
                        picking_obj.write(cr, uid, map(lambda x: x.id, order.picking_ids), {'invoice_state': 'invoiced'})
                    cr.execute('insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)', (order.id, res))
        return res
sale_order()

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}
        lang = lang or context.get('lang',False)
        if not  partner_id:
            raise osv.except_osv(_('No Customer Defined !'), _('You have to select a customer in the sales form !\nPlease set one customer before choosing a product.'))
        warning = {}
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'lang': lang, 'partner_id': partner_id}
        if partner_id:
            lang = partner_obj.browse(cr, uid, partner_id).lang
        context_partner = {'lang': lang, 'partner_id': partner_id}

        if not product:
            return {'value': {'th_weight': 0, 'product_packaging': False,
                'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        if not date_order:
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        res = self.product_packaging_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, packaging, context=context)
        result = res.get('value', {})
        warning_msgs = res.get('warning') and res['warning']['message'] or ''
        product_obj = product_obj.browse(cr, uid, product, context=context)

        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if uos:
            if product_obj.uos_id:
                uos2 = product_uom_obj.browse(cr, uid, uos)
                if product_obj.uos_id.category_id.id != uos2.category_id.id:
                    uos = False
            else:
                uos = False
        if product_obj.description_sale:
            result['notes'] = product_obj.description_sale
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        if update_tax: #The quantity only have changed
            result['delay'] = (product_obj.sale_delay or 0.0)
            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)
            result.update({'type': product_obj.procure_method})

        if not flag:
            result['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
        domain = {}
        if (not uom) and (not uos):
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
                uos_category_id = False
            result['th_weight'] = qty * product_obj.weight
            domain = {'product_uom':
                        [('category_id', '=', product_obj.uom_id.category_id.id)],
                        'product_uos':
                        [('category_id', '=', uos_category_id)]}

        elif uos and not uom: # only happens if uom is False
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
        elif uom: # whether uos is set or not
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
            result['th_weight'] = q * product_obj.weight        # Round the quantity up

        if not uom2:
            uom2 = product_obj.uom_id
        compare_qty = float_compare(product_obj.virtual_available * uom2.factor, qty * product_obj.uom_id.factor, precision_rounding=product_obj.uom_id.rounding)
        if (product_obj.type=='product') and int(compare_qty) == -1 \
          and (product_obj.procure_method=='make_to_stock'):
            warn_msg = _('You plan to sell %.2f %s but you only have %.2f %s available !\nThe real stock is %.2f %s. (without reservations)') % \
                    (qty, uom2 and uom2.name or product_obj.uom_id.name,
                     max(0,product_obj.virtual_available), product_obj.uom_id.name,
                     max(0,product_obj.qty_available), product_obj.uom_id.name)
            warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"
        # get unit price

        if not pricelist:
            warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
                    'Please set one before choosing a product.')
            warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
        else:
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                    product, qty or 1.0, partner_id, {
                        'uom': uom or result.get('product_uom'),
                        'date': date_order,
                        })[pricelist]
            if price is False:
                warn_msg = _("Couldn't find a pricelist line matching this product and quantity.\n"
                        "You have to change either the product, the quantity or the pricelist.")

                warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
            else:
                result.update({'price_unit': price})
        if warning_msgs:
            warning = {
                       'title': _('Configuration Error !'),
                       'message' : warning_msgs
                    }
        return {'value': result, 'domain': domain, 'warning': warning}
    
#    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
#            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
#        if not  partner_id:
#            raise osv.except_osv(_('No Customer Defined !'), _('You have to select a customer in the sales form !\nPlease set one customer before choosing a product.'))
#        warning = {}
#        product_uom_obj = self.pool.get('product.uom')
#        partner_obj = self.pool.get('res.partner')
#        product_obj = self.pool.get('product.product')
#        if partner_id:
#            lang = partner_obj.browse(cr, uid, partner_id).lang
#        context = {'lang': lang, 'partner_id': partner_id}
#
#        if not product:
#            return {'value': {'th_weight': 0, 'product_packaging': False,
#                'product_uos_qty': qty, 'tax_id':[]}, 'domain': {'product_uom': [],
#                   'product_uos': []}}
#        if not date_order:
#            date_order = time.strftime('%Y-%m-%d')
#
#        result = {}
#        product_obj = product_obj.browse(cr, uid, product, context=context)
#        if not packaging and product_obj.packaging:
#            packaging = product_obj.packaging[0].id
#            result['product_packaging'] = packaging
#
#        if packaging:
#            default_uom = product_obj.uom_id and product_obj.uom_id.id
#            pack = self.pool.get('product.packaging').browse(cr, uid, packaging, context=context)
#            q = product_uom_obj._compute_qty(cr, uid, uom, pack.qty, default_uom)
##            qty = qty - qty % q + q
#            if qty and (q and not (qty % q) == 0):
#                ean = pack.ean or _('(n/a)')
#                qty_pack = pack.qty
#                type_ul = pack.ul
#                warn_msg = _("You selected a quantity of %d Units.\n"
#                            "But it's not compatible with the selected packaging.\n"
#                            "Here is a proposition of quantities according to the packaging:\n\n"
#                            "EAN: %s Quantity: %s Type of ul: %s") % \
#                                (qty, ean, qty_pack, type_ul.name)
#                warning = {
#                    'title': _('Picking Information !'),
#                    'message': warn_msg
#                    }
#            result['product_uom_qty'] = qty
#
#        uom2 = False
#        if uom:
#            uom2 = product_uom_obj.browse(cr, uid, uom)
#            if product_obj.uom_id.category_id.id != uom2.category_id.id:
#                uom = False
#        if uos:
#            if product_obj.uos_id:
#                uos2 = product_uom_obj.browse(cr, uid, uos)
#                if product_obj.uos_id.category_id.id != uos2.category_id.id:
#                    uos = False
#            else:
#                uos = False
#        if product_obj.description_sale:
#            result['notes'] = product_obj.description_sale
#        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
#        if update_tax: #The quantity only have changed
#            result['delay'] = (product_obj.sale_delay or 0.0)
#            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)
#            result.update({'type': product_obj.procure_method})
#
#        if not flag:
#            result['name'] = self.pool.get('product.product').browse(cr, uid, [product_obj.id], context=context)[0]['description']
#            
#        domain = {}
#        if (not uom) and (not uos):
#            result['product_uom'] = product_obj.uom_id.id
#            if product_obj.uos_id:
#                result['product_uos'] = product_obj.uos_id.id
#                result['product_uos_qty'] = qty * product_obj.uos_coeff
#                uos_category_id = product_obj.uos_id.category_id.id
#            else:
#                result['product_uos'] = False
#                result['product_uos_qty'] = qty
#                uos_category_id = False
#            result['th_weight'] = qty * product_obj.weight
#            domain = {'product_uom':
#                        [('category_id', '=', product_obj.uom_id.category_id.id)],
#                        'product_uos':
#                        [('category_id', '=', uos_category_id)]}
#
#        elif uos and not uom: # only happens if uom is False
#            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
#            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
#            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
#        elif uom: # whether uos is set or not
#            default_uom = product_obj.uom_id and product_obj.uom_id.id
#            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
#            if product_obj.uos_id:
#                result['product_uos'] = product_obj.uos_id.id
#                result['product_uos_qty'] = qty * product_obj.uos_coeff
#            else:
#                result['product_uos'] = False
#                result['product_uos_qty'] = qty
#            result['th_weight'] = q * product_obj.weight        # Round the quantity up
#
#        if not uom2:
#            uom2 = product_obj.uom_id
#        if (product_obj.type=='product') and (product_obj.virtual_available * uom2.factor < qty * product_obj.uom_id.factor) \
#          and (product_obj.procure_method=='make_to_stock'):
#            warning = {
#                'title': _('Not enough stock !'),
#                'message': _('You plan to sell %.2f %s but you only have %.2f %s available !\nThe real stock is %.2f %s. (without reservations)') %
#                    (qty, uom2 and uom2.name or product_obj.uom_id.name,
#                     max(0,product_obj.virtual_available), product_obj.uom_id.name,
#                     max(0,product_obj.qty_available), product_obj.uom_id.name)
#            }
#        # get unit price
#        if not pricelist:
#            warning = {
#                'title': 'No Pricelist !',
#                'message':
#                    'You have to select a pricelist or a customer in the sales form !\n'
#                    'Please set one before choosing a product.'
#                }
#        else:
#            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
#                    product, qty or 1.0, partner_id, {
#                        'uom': uom,
#                        'date': date_order,
#                        })[pricelist]
#            if price is False:
#                warning = {
#                    'title': 'No valid pricelist line found !',
#                    'message':
#                        "Couldn't find a pricelist line matching this product and quantity.\n"
#                        "You have to change either the product, the quantity or the pricelist."
#                    }
#            else:
#                result.update({'price_unit': price})
#        return {'value': result, 'domain': domain, 'warning': warning}
    
sale_order_line()
