from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from lxml import etree

class partial_serialized_product(osv.osv_memory):

    _name = 'partial.serialized.product'

    _columns = {
            
            'name':fields.date('Order Date',readonly=True),
            'qty':fields.float('Quantity',digits=(16,2),readonly=True),
            'product_id':fields.many2one('product.product','Product'),
            'line_ids':fields.one2many('partial.serialized.line','serialized_id','Serial No. Line'),
            }
    
    def default_get(self, cr, uid, fields, context=None):
        res={}
        if not context:
            return res
        incm_id = context.get('active_ids', [])
        res = super(partial_serialized_product, self).default_get(cr, uid, fields, context=context)
        product_line = []
        if incm_id:
            for rec in self.pool.get('stock.partial.move').browse(cr, uid, incm_id):
                i = 1
                for line in rec.move_ids:
                    if line.product_id.serialized:
                        if 'product_id' in fields:
                            res.update({'product_id' : line.product_id.id})
                        if 'qty' in fields:
                            res.update({'qty' : line.quantity})
                        i+=1
                
                if 'name' in fields:
                    res.update({'name':time.strftime('%Y-%m-%d')})
        return res
    
    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        result = super(partial_serialized_product, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
        if view_type == 'form':
            incm_id = context.get('active_ids', False)
            doc = etree.XML(result['arch'])
            _moves_fields = result['fields']
            _moves_arch_lst = """
                                <form string="Serializing Products" version="7.0">
                                """
            for rec in self.pool.get('stock.partial.move').browse(cr, uid, incm_id):
                for line in rec.move_ids:
                    if line.product_id.serialized:
                        _moves_arch_lst += """
                                    <group col="4" colspan="4">
                                    <separator string="Enter %s serial number for product %s" colspan="4"/>
                                    <field name="line_ids" nolabel="1" colspan="4"/>
                                    </group>""" % (line.quantity,line.product_id.name)
                
                    _moves_fields.update({
                    "line_ids" : {'string': 'Serial No. Line','type': 'one2many','relation':'partial.serialized.line'},
                    "product_id" : {'string': 'Product','type': 'many2one','relation':'product.product','required':True},
                    "qty" : {'string': 'Quantity','type': 'float','required':True},                
                    })
                    
                    _moves_arch_lst += """
                                        <newline/>
                                        """
                   
            
            _moves_arch_lst +="""<separator colspan="4"/>
                                   <group col="4" colspan="4">
                                   <button special="cancel" icon="gtk-cancel" string="Cancel" />
                                   <button name="return_do_partial" icon="gtk-ok" string="Approved" type="object"/>
                                   </group>
                                </form>
                                """
            result['arch'] = _moves_arch_lst
            result['fields'] = _moves_fields
        return result
    
    def return_do_partial(self, cr, uid, ids, context=None):
        if context is None: context = {}
        move_id = context.get('active_ids',[])
        field = ['qty','product_id','line_ids']
        for rec in self.read(cr, uid, ids, field):
            if rec['product_id'] == False:
                break
            if int(rec['qty']) <> len(rec['line_ids']):
                raise osv.except_osv(('Warning !'),('Total quantity and number of serial lines doesnot match.' ))
       
            for line in self.pool.get('partial.serialized.line').browse(cr, uid, rec['line_ids']):
                if rec['product_id']:      
                    try:
                        self.pool.get('product.serialize').create(cr, uid, {'product_id':rec['product_id'][0],'name':line.serial_no})
                    except:
                        raise osv.except_osv(('Duplicate key value violates unique constraint !'),('Serial number '+ line.serial_no +' is already exist, please enter unique serial number.' ))
           
        return self.pool.get('stock.partial.move').do_partial(cr, uid, move_id, context=context)
    
partial_serialized_product()


class partial_serialized_line(osv.osv_memory):

    _name = 'partial.serialized.line'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('partial.serialized.product','Serial No',ondelete='cascade'),
        }
    
partial_serialized_line()
