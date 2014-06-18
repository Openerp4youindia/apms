from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class type_invoice(osv.osv):
    _name = 'type.invoice'
    
    _columns = {
                'name':fields.char('Invoice Type',size=64,required=True),
                'report':fields.selection([('Retail Invoice Delhi','Retail Invoice Delhi'),('Tax Invoice Delhi','Tax Invoice Delhi'),('Retail Invoice Bangalore','Retail Invoice Bangalore'),('Tax Invoice Bangalore','Tax Invoice Bangalore')],'Type Of Report',required=True),
                'journal_id': fields.many2one('account.journal', 'Journal', required=True),
               
                }

    _sql_constraints=[('type_invoice_unique','UNIQUE(report,journal_id)','Journal must be unique per invoice type.!')]

type_invoice()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def get_report_id(self, cr, uid, ids ,context=None):
        if not context:
            context = {}
            return context
        inv_id = context.get('active_ids',[])
        report_obj = self.pool.get('ir.actions.report.xml')
        inv_obj = self.pool.get('account.invoice')
        datas = {'ids' : ids}
        type_inv = self.read(cr, uid, ids)
        for inv in self.browse(cr, uid, ids):
            if inv.invoice_type_id and inv.invoice_type_id.report == 'Retail Invoice Delhi':
                report_name = 'genius.retail.invoice.delhi'
            elif inv.invoice_type_id and inv.invoice_type_id.report == 'Tax Invoice Delhi':
                if not inv.partner_id.tin_no:
                    raise osv.except_osv(_('Configuration Error !'),
                            _('Please enter party tin to generate Tax Invoice report.'))
                report_name = 'genius.tax.invoice.delhi'
            elif inv.invoice_type_id and inv.invoice_type_id.report == 'Retail Invoice Bangalore':
                report_name = 'genius.retail.invoice.bang'
            elif inv.invoice_type_id and inv.invoice_type_id.report == 'Tax Invoice Bangalore':
                if not inv.partner_id.tin_no:
                    raise osv.except_osv(_('Configuration Error !'),
                            _('Please enter party tin to generate Tax Invoice report.'))
                report_name = 'genius.tax.invoice.bang'
            else:
                report_name = 'account.invoice'

        
        
        return {
            'type' : 'ir.actions.report.xml',
            'report_name':report_name,
            'datas' : datas,
            'nodestroy':True,
        }
    

    
    def _amount_all(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'total_weight':0.0,
            }
            for line in invoice.invoice_line:
                res[invoice.id]['total_weight'] += line.quantity * (line.product_id and line.product_id.weight or 0.0)
                res[invoice.id]['amount_untaxed'] += line.price_subtotal            
            for line in invoice.tax_line:
                res[invoice.id]['amount_tax'] += line.amount
            res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']
        return res
 
    _columns = {
            'note': fields.text('Internal Notes'),
            'printed_note': fields.text('Printed Notes'),
            'address_shipping_id': fields.many2one('res.partner.address', 'Shipping Address', readonly=True, states={'draft': [('readonly', False)]}, help="Shipping address for current sales order."),
            'purch_number':fields.char('Purchase Order/Number',size=64),
            'purch_date':fields.date('Purchase Order/date'),
            'total_weight': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Weight', store=True, multi='all'),
            'shipping_cost':fields.float('Shipping Cost',digits=(16,2),readonly=True),
            'carrier_id':fields.many2one('res.partner','Carrier'),
	        'sale_id':fields.many2one('sale.order','Sale Order'),
            'invoice_type_id':fields.many2one('type.invoice','Invoice Type', readonly=True, states={'draft':[('readonly',False)]}, select=True),
        }
    
    _defaults={
               'address_shipping_id': lambda self, cr, uid, context: context.get('partner_id', False) and self.pool.get('res.partner').address_get(cr, uid, [context['partner_id']], ['delivery'])['delivery'],
               }

    
    
    def onchange_invoice_type(self, cr, uid, ids, invoice_type_id, context=None):
        res = {}
        res['value'] = {}
        if not invoice_type_id:
            return {'value':{'journal_id':False}}
        for rec in self.pool.get('type.invoice').browse(cr, uid, [invoice_type_id]):
            res['value'] = {'journal_id':rec.journal_id and rec.journal_id.id or False}

        return res
                
    
    def button_reset_taxes(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        ait_obj = self.pool.get('account.invoice.tax')
        for id in ids:
            cr.execute("DELETE FROM account_invoice_tax WHERE invoice_id=%s AND manual is False", (id,))
            partner = self.browse(cr, uid, id, context=ctx).partner_id
            if partner.lang:
                ctx.update({'lang': partner.lang})
            for taxe in ait_obj.compute(cr, uid, id, context=ctx).values():
                ait_obj.create(cr, uid, taxe)
        # Update the stored value (fields.function), so we write to trigger recompute
        self.pool.get('account.invoice').write(cr, uid, ids, {'invoice_line':[],'shipping_cost':0.0}, context=ctx)
        
        return True
    
    def onchange_partner_id(self, cr, uid, ids, type, partner_id,\
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        invoice_addr_id = False
        contact_addr_id = False
        delivery_addr_id = False
        partner_payment_term = False
        acc_id = False
        bank_id = False
        fiscal_position = False

        opt = [('uid', str(uid))]
        if partner_id:

            opt.insert(0, ('id', partner_id))
            res = self.pool.get('res.partner').address_get(cr, uid, [partner_id], ['contact', 'invoice','delivery'])
            contact_addr_id = res['contact']
            invoice_addr_id = res['invoice']
            delivery_addr_id = res['delivery']
            p = self.pool.get('res.partner').browse(cr, uid, partner_id)
            if company_id:
                if p.property_account_receivable.company_id.id != company_id and p.property_account_payable.company_id.id != company_id:
                    property_obj = self.pool.get('ir.property')
                    rec_pro_id = property_obj.search(cr,uid,[('name','=','property_account_receivable'),('res_id','=','res.partner,'+str(partner_id)+''),('company_id','=',company_id)])
                    pay_pro_id = property_obj.search(cr,uid,[('name','=','property_account_payable'),('res_id','=','res.partner,'+str(partner_id)+''),('company_id','=',company_id)])
                    if not rec_pro_id:
                        rec_pro_id = property_obj.search(cr,uid,[('name','=','property_account_receivable'),('company_id','=',company_id)])
                    if not pay_pro_id:
                        pay_pro_id = property_obj.search(cr,uid,[('name','=','property_account_payable'),('company_id','=',company_id)])
                    rec_line_data = property_obj.read(cr,uid,rec_pro_id,['name','value_reference','res_id'])
                    pay_line_data = property_obj.read(cr,uid,pay_pro_id,['name','value_reference','res_id'])
                    rec_res_id = rec_line_data and rec_line_data[0].get('value_reference',False) and int(rec_line_data[0]['value_reference'].split(',')[1]) or False
                    pay_res_id = pay_line_data and pay_line_data[0].get('value_reference',False) and int(pay_line_data[0]['value_reference'].split(',')[1]) or False
                    if not rec_res_id and not pay_res_id:
                        raise osv.except_osv(_('Configuration Error !'),
                            _('Can not find account chart for this company, Please Create account.'))
                    account_obj = self.pool.get('account.account')
                    rec_obj_acc = account_obj.browse(cr, uid, [rec_res_id])
                    pay_obj_acc = account_obj.browse(cr, uid, [pay_res_id])
                    p.property_account_receivable = rec_obj_acc[0]
                    p.property_account_payable = pay_obj_acc[0]

            if type in ('out_invoice', 'out_refund'):
                acc_id = p.property_account_receivable.id
            else:
                acc_id = p.property_account_payable.id
            fiscal_position = p.property_account_position and p.property_account_position.id or False
            partner_payment_term = p.property_payment_term and p.property_payment_term.id or False
            if p.bank_ids:
                bank_id = p.bank_ids[0].id

        result = {'value': {
            'address_contact_id': contact_addr_id,
            'address_invoice_id': invoice_addr_id,
            'address_shipping_id':delivery_addr_id,
            'account_id': acc_id,
            'payment_term': partner_payment_term,
            'fiscal_position': fiscal_position
            }
        }

        if type in ('in_invoice', 'in_refund'):
            result['value']['partner_bank_id'] = bank_id

        if payment_term != partner_payment_term:
            if partner_payment_term:
                to_update = self.onchange_payment_term_date_invoice(
                    cr, uid, ids, partner_payment_term, date_invoice)
                result['value'].update(to_update['value'])
            else:
                result['value']['date_due'] = False

        if partner_bank_id != bank_id:
            to_update = self.onchange_partner_bank(cr, uid, ids, bank_id)
            result['value'].update(to_update['value'])
        return result
    
    def update_picking(self, cr, uid, ids, context=None):
        res = {}
        stock_obj = self.pool.get('stock.move')
        for inv in self.browse(cr, uid, ids):
            if inv.sale_id:
                for pick in inv.sale_id.picking_ids: 
                    for invline in inv.invoice_line:
                        match = False
                        match_product = False
                        for line in pick.move_lines:
                            if line.product_id and line.product_id.id == invline.product_id.id and line.product_qty == invline.quantity:
                                if not match:
                                    match = True
                            elif line.product_id and line.product_id.id == invline.product_id.id:
                                if not match and not match_product:
                                    match_product = True
                                    match = True
                                
                        for line in pick.move_lines:
                            if match:
                                if invline.product_id and invline.product_id.serialized:
                                    if line.product_id and line.product_id.id == invline.product_id.id and line.product_qty == invline.quantity:
                                        stock_obj.write(cr, uid, [line.id],{'serialize_ids':[(6,0,[x.id for x in invline.serialize_ids])]})
                                        
                            if match_product:
                                if invline.product_id and invline.product_id.serialized:
                                    if line.product_id and line.product_id.id == invline.product_id.id:
                                        stock_obj.write(cr, uid, [line.id],{'product_qty':invline.quantity,'serialize_ids':[(6,0,[x.id for x in invline.serialize_ids])]})
                                        
                            if not match:
                                location_id = inv.sale_id.shop_id.warehouse_id.lot_stock_id.id
                                output_id = inv.sale_id.shop_id.warehouse_id.lot_output_id.id
                                date_planned = datetime.strptime(inv.sale_id.date_order, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(0.0)    
                                date_planned = (date_planned - timedelta(days=inv.company_id.security_lead)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                                
                                stock = {
                                    'name': invline.name[:250],
                                    'picking_id': pick.id,
                                    'product_id': invline.product_id and invline.product_id.id,
                                    'date': date_planned,
                                    'date_expected': date_planned,
                                    'product_qty': invline.quantity,
                                    'product_uom': invline.uos_id and invline.uos_id.id or False,
                                    'product_uos_qty': invline.quantity,
                                    'product_uos': invline.uos_id and invline.uos_id.id or False,
                                    'address_id': inv.address_shipping_id and inv.address_shipping_id.id or inv.address_invoice_id and inv.address_invoice_id.id or False,
                                    'location_id': location_id,
                                    'location_dest_id': output_id,
                                    'tracking_id': False,
                                    'state': 'waiting',
                                    'note': invline.note,
                                    'company_id': inv.company_id.id,
                                    'price_unit': invline.price_unit or 0.0,
                                    
                                    }
                                
                                stock_id = stock_obj.create(cr, uid, stock)
                                if stock_id:
                                    stock_obj.write(cr, uid, stock_id,{'serialize_ids':[(6,0,[x.id for x in invline.serialize_ids])]})

                    message = _("The delivery order '%s' has been updated.") % (pick.name,)
                    self.log(cr, uid, inv.id, message)

        return res
    
    def cancel_picking(self, cr, uid, ids, context=None):
        res = {}
        stock_obj = self.pool.get('stock.move')
        for inv in self.browse(cr, uid, ids):
            if inv.sale_id:
                for pick in inv.sale_id.picking_ids:
                    for line in pick.move_lines:
                        for invline in inv.invoice_line:
                            if invline.product_id and invline.product_id.serialized:
                                if line.product_id and line.product_id.id == invline.product_id.id and line.product_qty == invline.quantity:
                                    stock_obj.write(cr, uid, [line.id],{'serialize_ids':[(6,0,[])]})
    
        return res

    def create_purchase_order(self, cr, uid, ids, context=None):
        res = {}
        for inv in self.browse(cr, uid, ids):
            pur = {
                    'origin': inv.number,
                    'date_order': time.strftime('%Y-%m-%d'),
                    'partner_id': inv.partner_id.id,
                    'partner_address_id': inv.address_invoice_id and inv.address_invoice_id.id or False,
                    'contact_address_id':inv.address_contact_id and inv.address_contact_id.id or False,
                    'pricelist_id': inv.partner_id.property_product_pricelist_purchase and inv.partner_id.property_product_pricelist_purchase.id or False,
                    'state': 'draft',
                    'order_line': {},
                    'notes': inv.comment or '',
                    'printed_note': inv.printed_note or '',
                    'fiscal_position': inv.fiscal_position and inv.fiscal_position.id or False,
                    'location_id':inv.partner_id.property_stock_customer and inv.partner_id.property_stock_customer.id or False,
                   }
            self.pool.get('purchase.order').create(cr, uid, pur)
            self.update_picking(cr, uid, ids, context=context)
            message = _("New purchase order has been created.")
            self.log(cr, uid, inv.id, message)

        return res

    def create_incoming_picking(self, cr, uid, ids, context=None):
        res = {}
        pick_obj = self.pool.get('stock.picking')
        stock_obj = self.pool.get('stock.move')
        for inv in self.browse(cr, uid, ids):
            if inv.sale_id:
                for pick in pick_obj.browse(cr, uid, pick_obj.search(cr, uid, [('sale_id','=',inv.sale_id.id),('state','!=','cancel')])):
                    name = pick.name
                    stock_journal_id = pick.stock_journal_id and pick.stock_journal_id.id or False
                location_id = inv.sale_id.shop_id.warehouse_id.lot_stock_id.id
                output_id = inv.sale_id.shop_id.warehouse_id.lot_output_id.id
                date_planned = datetime.strptime(inv.sale_id.date_order, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(0.0)    
                date_planned = (date_planned - timedelta(days=inv.company_id.security_lead)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                
                inpick = {
                        'name': name + 'return',
                        'origin': inv.sale_id.name,
                        'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                        'type': 'in',
                        'address_id': inv.address_shipping_id and inv.address_shipping_id.id or inv.address_invoice_id and inv.address_invoice_id.id or False,
                        'invoice_state':'none',
                        'sale_id': inv.sale_id.id,
                        'company_id': inv.company_id.id,
                        'move_lines' : [],
                        'stock_journal_id':stock_journal_id,
                        'return_picking':True,
                    }
                pick_id = pick_obj.create(cr, uid, inpick)
                for invline in inv.invoice_line:
                    stock = {
                        'name': invline.name[:250],
                        'picking_id': pick_id,
                        'product_id': invline.product_id and invline.product_id.id,
                        'date': date_planned,
                        'date_expected': date_planned,
                        'product_qty': invline.quantity,
                        'product_uom': invline.uos_id and invline.uos_id.id or False,
                        'product_uos_qty': invline.quantity,
                        'product_uos': invline.uos_id and invline.uos_id.id or False,
                        'address_id': inv.address_shipping_id and inv.address_shipping_id.id or inv.address_invoice_id and inv.address_invoice_id.id or False,
                        'location_id': output_id,
                        'location_dest_id': location_id,
                        'tracking_id': False,
                        'state': 'draft',
                        'note': invline.note or '',
                        'company_id': inv.company_id.id,
                        'price_unit': invline.price_unit or 0.0,
                        
                        }
                
                    stock_id = stock_obj.create(cr, uid, stock)
                    if stock_id:
                        stock_obj.write(cr, uid, stock_id,{'serialize_ids':[(6,0,[x.id for x in invline.serialize_ids])]})

                message = _("The incoming shipment order '%s' return has been created.") % (name,)
                self.log(cr, uid, inv.id, message)


        return res
    
    def action_number(self, cr, uid, ids, context=None):
        pick_obj = self.pool.get('stock.picking')
        if context is None:
            context = {}
        #TODO: not correct fix but required a frech values before reading it.
        self.write(cr, uid, ids, {})

        for obj_inv in self.browse(cr, uid, ids, context=context):
            for line in obj_inv.invoice_line:
                if obj_inv.type == 'out_invoice':
                    if line.product_id and line.product_id.serialized:
                        if line.product_id and line.quantity <> len(line.serialize_ids):
                            raise osv.except_osv(('Warning !'),('Total quantity %s and number of serial lines %s doesnot match for product %s.' )%(line.quantity, len(line.serialize_ids), line.product_id.name))
                        if line.product_id:
                            for serial in line.serialize_ids:
                                if serial.state:
                                    raise osv.except_osv(('Warning !'),('Serial number %s is already sold, Change the serial number to move forward.' )%(serial.name))
                        if line.product_id:
                            for serial in line.serialize_ids:
                                self.pool.get('product.serialize').write(cr, uid, [serial.id], {'state':True})
                                
                if obj_inv.type == 'out_refund':
                    if line.product_id and line.product_id.serialized:
                        if line.product_id and line.quantity <> len(line.serialize_ids):
                            raise osv.except_osv(('Warning !'),('Total quantity %s and number of serial lines %s doesnot match for product %s.' )%(line.quantity, len(line.serialize_ids), line.product_id.name))
                        if line.product_id:
                            for serial in line.serialize_ids:
                                if not serial.state:
                                    raise osv.except_osv(('Warning !'),('Serial number %s is not sold, Change the serial number to move forward.' )%(serial.name))
                        if line.product_id:
                            for serial in line.serialize_ids:
                                self.pool.get('product.serialize').write(cr, uid, [serial.id], {'state':False})
                            
            id = obj_inv.id
            invtype = obj_inv.type
            number = obj_inv.number
            move_id = obj_inv.move_id and obj_inv.move_id.id or False
            reference = obj_inv.reference or ''

            self.write(cr, uid, ids, {'internal_number':number})

            if invtype in ('in_invoice', 'in_refund'):
                if not reference:
                    ref = self._convert_ref(cr, uid, number)
                else:
                    ref = reference
            else:
                ref = self._convert_ref(cr, uid, number)

            cr.execute('UPDATE account_move SET ref=%s ' \
                    'WHERE id=%s AND (ref is null OR ref = \'\')',
                    (ref, move_id))
            cr.execute('UPDATE account_move_line SET ref=%s ' \
                    'WHERE move_id=%s AND (ref is null OR ref = \'\')',
                    (ref, move_id))
            cr.execute('UPDATE account_analytic_line SET ref=%s ' \
                    'FROM account_move_line ' \
                    'WHERE account_move_line.move_id = %s ' \
                        'AND account_analytic_line.move_id = account_move_line.id',
                        (ref, move_id))

            for inv_id, name in self.name_get(cr, uid, [id]):
                ctx = context.copy()
                if obj_inv.type in ('out_invoice', 'out_refund'):
                    ctx = self.get_log_context(cr, uid, context=ctx)
                message = _('Invoice ') + " '" + name + "' "+ _("is validated.")
                self.log(cr, uid, inv_id, message, context=ctx)
            if obj_inv.type == 'out_invoice':
                if obj_inv.carrier_id:
                    self.create_purchase_order(cr, uid, ids, context=context)
                else:
                    self.update_picking(cr, uid, ids, context=context)
            
            if obj_inv.type == 'out_refund':
                if obj_inv.sale_id:
                    self.create_incoming_picking(cr, uid, ids, context=context)
                
        return True
    def action_cancel(self, cr, uid, ids, *args):
        context = {} # TODO: Use context from arguments
        account_move_obj = self.pool.get('account.move')
        invoices = self.read(cr, uid, ids, ['move_id', 'payment_ids'])
        move_ids = [] # ones that we will need to remove
        for i in invoices:
            if i['move_id']:
                move_ids.append(i['move_id'][0])
            if i['payment_ids']:
                account_move_line_obj = self.pool.get('account.move.line')
                pay_ids = account_move_line_obj.browse(cr, uid, i['payment_ids'])
                for move_line in pay_ids:
                    if move_line.reconcile_partial_id and move_line.reconcile_partial_id.line_partial_ids:
                        raise osv.except_osv(_('Error !'), _('You can not cancel an invoice which is partially paid! You need to unreconcile related payment entries first!'))

        # First, set the invoices as cancelled and detach the move ids
        self.write(cr, uid, ids, {'state':'cancel', 'internal_number':False,'move_id':False})
        if move_ids:
            # second, invalidate the move(s)
            account_move_obj.button_cancel(cr, uid, move_ids, context=context)
            # delete the move this invoice was pointing to
            # Note that the corresponding move_lines and move_reconciles
            # will be automatically deleted too
            account_move_obj.unlink(cr, uid, move_ids, context=context)
        self._log_event(cr, uid, ids, -1.0, 'Cancel Invoice')
        for obj_inv in self.browse(cr, uid, ids, context=context):
            for line in obj_inv.invoice_line:
                    if line.product_id and line.product_id.serialized:
                        for serial in line.serialize_ids:
                            self.pool.get('product.serialize').write(cr, uid, [serial.id], {'state':False})
                            
        self.cancel_picking(cr, uid, ids)
        return True
    
    def action_proforma(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        for obj_inv in self.browse(cr, uid, ids, context=context):
            for line in obj_inv.invoice_line:
                if obj_inv.type == 'out_invoice':
                    if line.product_id and line.product_id.serialized:
                        if line.product_id and line.quantity <> len(line.serialize_ids):
                            raise osv.except_osv(('Warning !'),('Total quantity %s and number of serial lines %s doesnot match for product %s.' )%(line.quantity, len(line.serialize_ids), line.product_id.name))
                        if line.product_id:
                            for serial in line.serialize_ids:
                                if serial.state:
                                    raise osv.except_osv(('Warning !'),('Serial number %s is already sold, Change the serial number to move forward.' )%(serial.name))
                            
                if obj_inv.type == 'out_refund':
                    if line.product_id and line.product_id.serialized:
                        if line.product_id and line.quantity <> len(line.serialize_ids):
                            raise osv.except_osv(('Warning !'),('Total quantity %s and number of serial lines %s doesnot match for product %s.' )%(line.quantity, len(line.serialize_ids), line.product_id.name))
                        if line.product_id:
                            for serial in line.serialize_ids:
                                if not serial.state:
                                    raise osv.except_osv(('Warning !'),('Serial number %s is not sold, Change the serial number to move forward.' )%(serial.name))
              
                                
            self.write(cr, uid, ids, {'state':'proforma2'})
        return True     


    def _refund_cleanup_lines(self, cr, uid, lines):
        for line in lines:
            del line['id']
            del line['invoice_id']
            for field in ('company_id', 'partner_id', 'account_id', 'product_id',
                          'uos_id', 'account_analytic_id', 'tax_code_id', 'base_code_id'):
                if line.get(field):
                    line[field] = line[field][0]
            if 'invoice_line_tax_id' in line:
                line['invoice_line_tax_id'] = [(6,0, line.get('invoice_line_tax_id', [])) ]
                
            if 'serialize_ids' in line:
                line['serialize_ids'] = [(6,0, line.get('serialize_ids', [])) ]
        return map(lambda x: (0,0,x), lines)
    
    
    def refund(self, cr, uid, ids, date=None, period_id=None, description=None, journal_id=None):
        invoices = self.read(cr, uid, ids, ['name', 'type', 'number', 'reference', 'comment', 'date_due', 'partner_id', 'address_contact_id', 'address_invoice_id', 'partner_contact', 'partner_insite', 'partner_ref', 'payment_term', 'account_id', 'currency_id', 'invoice_line', 'tax_line', 'journal_id','sale_id','address_shipping_id'])
        obj_invoice_line = self.pool.get('account.invoice.line')
        obj_invoice_tax = self.pool.get('account.invoice.tax')
        obj_journal = self.pool.get('account.journal')
        new_ids = []
        for invoice in invoices:
            del invoice['id']

            type_dict = {
                'out_invoice': 'out_refund', # Customer Invoice
                'in_invoice': 'in_refund',   # Supplier Invoice
                'out_refund': 'out_invoice', # Customer Refund
                'in_refund': 'in_invoice',   # Supplier Refund
            }

            invoice_lines = obj_invoice_line.read(cr, uid, invoice['invoice_line'])
            invoice_lines = self._refund_cleanup_lines(cr, uid, invoice_lines)

            tax_lines = obj_invoice_tax.read(cr, uid, invoice['tax_line'])
            tax_lines = filter(lambda l: l['manual'], tax_lines)
            tax_lines = self._refund_cleanup_lines(cr, uid, tax_lines)
            if journal_id:
                refund_journal_ids = [journal_id]
            elif invoice['type'] == 'in_invoice':
                refund_journal_ids = obj_journal.search(cr, uid, [('type','=','purchase_refund')])
            else:
                refund_journal_ids = obj_journal.search(cr, uid, [('type','=','sale_refund')])

            if not date:
                date = time.strftime('%Y-%m-%d')
            invoice.update({
                'type': type_dict[invoice['type']],
                'date_invoice': date,
                'state': 'draft',
                'number': False,
                'invoice_line': invoice_lines,
                'tax_line': tax_lines,
                'journal_id': refund_journal_ids
            })
            if period_id:
                invoice.update({
                    'period_id': period_id,
                })
            if description:
                invoice.update({
                    'name': description,
                })
            # take the id part of the tuple returned for many2one fields
            for field in ('address_contact_id', 'address_invoice_id', 'partner_id',
                    'account_id', 'currency_id', 'payment_term', 'journal_id','sale_id','address_shipping_id'):
                invoice[field] = invoice[field] and invoice[field][0]
            # create the new invoice
            new_ids.append(self.create(cr, uid, invoice))

        return new_ids
              


account_invoice()

class account_invoice_line(osv.osv):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
    
    _columns={
              'serialize_ids':fields.many2many('product.serialize','invoice_serialize_rel','serial_id','invoice_id','Serial No.')
              }

    
    _defaults={
               'name':'Demo description',
               }

    
    
    def product_id_change(self, cr, uid, ids, product, uom, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, address_invoice_id=False, currency_id=False, context=None, company_id=None):
        if context is None:
            context = {}
        warning = {}
        company_id = company_id if company_id != None else context.get('company_id',False)
        context = dict(context)
        context.update({'company_id': company_id})
        if not partner_id:
            raise osv.except_osv(_('No Partner Defined !'),_("You must first select a partner !") )
        if not product:
            if type in ('in_invoice', 'in_refund'):
                return {'value': {}, 'domain':{'product_uom':[]}}
            else:
                return {'value': {'price_unit': 0.0,'serialize_ids':False}, 'domain':{'product_uom':[]}}
        part = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        fpos_obj = self.pool.get('account.fiscal.position')
        fpos = fposition_id and fpos_obj.browse(cr, uid, fposition_id, context=context) or False

        if part.lang:
            context.update({'lang': part.lang})
        result = {}
        res = self.pool.get('product.product').browse(cr, uid, product, context=context)

        if type in ('out_invoice','out_refund'):
            a = res.product_tmpl_id.property_account_income.id
            if not a:
                a = res.categ_id.property_account_income_categ.id
        else:
            a = res.product_tmpl_id.property_account_expense.id
            if not a:
                a = res.categ_id.property_account_expense_categ.id
        a = fpos_obj.map_account(cr, uid, fpos, a)
        if a:
            result['account_id'] = a

        if type in ('out_invoice', 'out_refund'):
            taxes = res.taxes_id and res.taxes_id or (a and self.pool.get('account.account').browse(cr, uid, a, context=context).tax_ids or False)
            if res.serialized:
                warning = {
                        'title': _('Serialize Information !'),
                        'message': _('You have selected a serialize product, Make sure to select serial number. !')
                        }
        else:
            taxes = res.supplier_taxes_id and res.supplier_taxes_id or (a and self.pool.get('account.account').browse(cr, uid, a, context=context).tax_ids or False)
        tax_id = fpos_obj.map_tax(cr, uid, fpos, taxes)

        if type in ('in_invoice', 'in_refund'):
            result.update( {'price_unit': price_unit or res.standard_price,'invoice_line_tax_id': tax_id} )
        else:
            result.update({'price_unit': res.list_price, 'invoice_line_tax_id': tax_id})
        result['name'] = res.partner_ref

        domain = {}
        result['uos_id'] = res.uom_id.id or uom or False
        result['note'] = res.description
        if result['uos_id']:
            res2 = res.uom_id.category_id.id
            if res2:
                domain = {'uos_id':[('category_id','=',res2 )]}
                
        

        res_final = {'value':result, 'domain':domain, 'warning':warning}

        if not company_id or not currency_id:
            return res_final

        company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
        currency = self.pool.get('res.currency').browse(cr, uid, currency_id, context=context)

        if company.currency_id.id != currency.id:
            if type in ('in_invoice', 'in_refund'):
                res_final['value']['price_unit'] = res.standard_price
            new_price = res_final['value']['price_unit'] * currency.rate
            res_final['value']['price_unit'] = new_price

        if uom:
            uom = self.pool.get('product.uom').browse(cr, uid, uom, context=context)
            if res.uom_id.category_id.id == uom.category_id.id:
                new_price = res_final['value']['price_unit'] * uom.factor_inv
                res_final['value']['price_unit'] = new_price
        return res_final
    
account_invoice_line()
