from dateutil.relativedelta import relativedelta
import time
import datetime

from openerp.osv import fields, osv
from openerp.tools.translate import _


class purchase_order(osv.osv):
    _inherit = 'purchase.order'
 
    _columns = {
	        'name': fields.char('Order Reference', size=64, readonly=True, select=True, help="unique number of the purchase order,computed automatically when the purchase order is created"),
            'printed_note': fields.text('Printed Notes'),
            'contact_address_id':fields.many2one('res.partner.address', 'Supplier Contact', 
                states={'confirmed':[('readonly',True)], 'approved':[('readonly',True)],'done':[('readonly',True)]},domain="[('partner_id', '=', partner_id)]"),
            'payment_term': fields.many2one('account.payment.term', 'Payment Term'),
            
        }
    
    _defaults={
               'contact_address_id': lambda self, cr, uid, context: context.get('partner_id', False) and  self.pool.get('res.partner').address_get(cr, uid, [context['partner_id']], ['contact'])['contact'],
               }

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        todo = []
        for po in self.browse(cr, uid, ids, context=context):
            if not po.order_line:
                raise osv.except_osv(_('Error !'),_('You cannot confirm a purchase order without any lines.'))
            for line in po.order_line:
                if line.state=='draft':
                    todo.append(line.id)
            if not po.name:
                name = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order')
            else:
                name = po.name
            message = _("Purchase order '%s' is confirmed.") % (name,)
            self.log(cr, uid, po.id, message)
#        current_name = self.name_get(cr, uid, ids)[0][1]
        self.pool.get('purchase.order.line').action_confirm(cr, uid, todo, context)
        for id in ids:
            self.write(cr, uid, [id], {'state' : 'confirmed', 'validator' : uid ,"name":name})
        return True
    
    def onchange_partner_id(self, cr, uid, ids, part):

        if not part:
            return {'value':{'partner_address_id': False,'contact_address_id':False,'payment_term':False, 'fiscal_position': False}}
        partner_obj = self.pool.get('res.partner')
        addr = partner_obj.address_get(cr, uid, [part], ['default'])
        contact_addr = partner_obj.address_get(cr, uid, [part], ['contact'])
        part = partner_obj.browse(cr, uid, part)
        pricelist = part.property_product_pricelist_purchase.id
        fiscal_position = part.property_account_position and part.property_account_position.id or False
        return {'value':{'partner_address_id': addr['default'],'contact_address_id': contact_addr['contact'], 'pricelist_id': pricelist, 'fiscal_position': fiscal_position}}
    
purchase_order()

class purchase_order_line(osv.osv):
    _inherit="purchase.order.line"
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=False, fiscal_position=False, date_planned=False,
            name=False, price_unit=False, notes=False):
        if not pricelist:
            raise osv.except_osv(_('No Pricelist !'), _('You have to select a pricelist or a supplier in the purchase form !\nPlease set one before choosing a product.'))
        if not  partner_id:
            raise osv.except_osv(_('No Partner!'), _('You have to select a partner in the purchase form !\nPlease set one partner before choosing a product.'))
        if not product:
            return {'value': {'price_unit': price_unit or 0.0, 'name': name or '',
                'notes': notes or'', 'product_uom' : uom or False}, 'domain':{'product_uom':[]}}
        res = {}
        prod= self.pool.get('product.product').browse(cr, uid, product)

        product_uom_pool = self.pool.get('product.uom')
        lang=False
        if partner_id:
            lang=self.pool.get('res.partner').read(cr, uid, partner_id, ['lang'])['lang']
        context={'lang':lang}
        context['partner_id'] = partner_id

        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
        prod_uom_po = prod.uom_po_id.id
        if not uom:
            uom = prod_uom_po
        if not date_order:
            date_order = time.strftime('%Y-%m-%d')
        qty = qty or 1.0
        seller_delay = 0

        prod_name = self.pool.get('product.product').browse(cr, uid, [prod.id], context=context)[0]['description']
        res = {}
        for s in prod.seller_ids:
            if s.name.id == partner_id:
                seller_delay = s.delay
                if s.product_uom:
                    temp_qty = product_uom_pool._compute_qty(cr, uid, s.product_uom.id, s.min_qty, to_uom_id=prod.uom_id.id)
                    uom = s.product_uom.id #prod_uom_po
                temp_qty = s.min_qty # supplier _qty assigned to temp
                if qty < temp_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    qty = temp_qty
                    res.update({'warning': {'title': _('Warning'), 'message': _('The selected supplier has a minimal quantity set to %s, you cannot purchase less.') % qty}})
        qty_in_product_uom = product_uom_pool._compute_qty(cr, uid, uom, qty, to_uom_id=prod.uom_id.id)
        price = self.pool.get('product.pricelist').price_get(cr,uid,[pricelist],
                    product, qty_in_product_uom or 1.0, partner_id, {
                        'uom': uom,
                        'date': date_order,
                        })[pricelist]
        dt = (datetime.now() + relativedelta(days=int(seller_delay) or 0.0)).strftime('%Y-%m-%d %H:%M:%S')


        res.update({'value': {'price_unit': price, 'name': prod_name,
            'taxes_id':map(lambda x: x.id, prod.supplier_taxes_id),
            'date_planned': date_planned or dt,'notes': notes or prod.description_purchase,
            'product_qty': qty,
            'product_uom': uom}})
        domain = {}

        taxes = self.pool.get('account.tax').browse(cr, uid,map(lambda x: x.id, prod.supplier_taxes_id))
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        res['value']['taxes_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, taxes)

        res2 = self.pool.get('product.uom').read(cr, uid, [uom], ['category_id'])
        res3 = prod.uom_id.category_id.id
        domain = {'product_uom':[('category_id','=',res2[0]['category_id'][0])]}
        if res2[0]['category_id'][0] != res3:
            raise osv.except_osv(_('Wrong Product UOM !'), _('You have to select a product UOM in the same category than the purchase UOM of the product'))

        res['domain'] = domain
        return res
    
purchase_order_line()
