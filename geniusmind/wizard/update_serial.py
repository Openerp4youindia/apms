from openerp.osv import osv
from openerp.osv import fields

class update_serial_wiz(osv.osv_memory):

    _name = 'update.serial.wiz'
 
    _columns = {
            
              'name':fields.char('Serial Number.',size=64,required=True),
              'state':fields.boolean('Sold',required=True),
              'product_id':fields.many2one('product.product','Product',required=True),
        }
    
    def default_get(self, cr, uid, fields, context=None):
        if not context:
            context = {}
        serial_id = context.get('active_ids',[])
        res = super(update_serial_wiz, self).default_get(cr, uid, fields, context=context)
        for rec in self.pool.get('product.serialize').browse(cr, uid, serial_id):
            if 'name' in fields:
                res.update({'name':rec.name})
            if 'product_id' in fields:
                res.update({'product_id':rec.product_id and rec.product_id.id or False})
            if 'state' in fields:
                res.update({'state':rec.state})
        return res
    
    def update_serial(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        serial_id = context.get('active_ids',[])
        for rec in self.browse(cr, uid, ids):            
            self.pool.get('product.serialize').write(cr, uid, serial_id,
            {'name':rec.name, 'product_id':rec.product_id and rec.product_id.id or False, 'state':rec.state })
        
            
        return {'type': 'ir.actions.act_window_close'}
    
update_serial_wiz()