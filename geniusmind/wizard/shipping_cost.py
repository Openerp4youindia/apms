from openerp.osv import osv
from openerp.osv import fields

class shipping_cost(osv.osv):

    _name = 'shipping.cost'
    
 
    _columns = {
            'name':fields.many2one('res.partner','Carrier',required=True,domain="[('supplier','=','1')]"),
            'zone_id':fields.many2one('shipping.zone','Zone',required=True),
            'weight':fields.float('Weight',digits=(16,2),required=True),
        }
    
    def default_get(self, cr, uid, fields, context=None):
        if not context:
            context = {}
        invoice_ids = context.get('active_ids',[])
        res = super(shipping_cost, self).default_get(cr, uid, fields, context=context)
        for rec in self.pool.get('account.invoice').browse(cr, uid, invoice_ids):
            if 'weight' in fields:
                res.update({'weight':rec.total_weight})
        return res
    
    def shipping_cost(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        invoice_ids = context.get('active_ids',[])
        for rec in self.browse(cr, uid, ids):            
            self.pool.get('account.invoice').write(cr, uid, invoice_ids,
            {'total_weight':rec.weight, 'shipping_cost':rec.weight * rec.zone_id.price, 'carrier_id':rec.name.id })
        
            
        return {'type': 'ir.actions.act_window_close'}
                
shipping_cost()