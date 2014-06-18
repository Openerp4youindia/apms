from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from lxml import etree

class picking_serialized_product(osv.osv_memory):

    _name = 'picking.serialized.product'
 
    _columns = {
            
            'name':fields.date('Order Date',readonly=True),
            'qty1':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty2':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty3':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty4':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty5':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty6':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty7':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty8':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty9':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty10':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty11':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty12':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty13':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty14':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty15':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty16':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty17':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty18':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty19':fields.float('Quantity',digits=(16,2),readonly=True),
            'qty20':fields.float('Quantity',digits=(16,2),readonly=True),
            'product_id1':fields.many2one('product.product','Product',readonly=True),
            'product_id2':fields.many2one('product.product','Product',readonly=True),
            'product_id3':fields.many2one('product.product','Product',readonly=True),
            'product_id4':fields.many2one('product.product','Product',readonly=True),
            'product_id5':fields.many2one('product.product','Product',readonly=True),
            'product_id6':fields.many2one('product.product','Product',readonly=True),
            'product_id7':fields.many2one('product.product','Product',readonly=True),
            'product_id8':fields.many2one('product.product','Product',readonly=True),
            'product_id9':fields.many2one('product.product','Product',readonly=True),
            'product_id10':fields.many2one('product.product','Product',readonly=True),
            'product_id11':fields.many2one('product.product','Product',readonly=True),
            'product_id12':fields.many2one('product.product','Product',readonly=True),
            'product_id13':fields.many2one('product.product','Product',readonly=True),
            'product_id14':fields.many2one('product.product','Product',readonly=True),
            'product_id15':fields.many2one('product.product','Product',readonly=True),
            'product_id16':fields.many2one('product.product','Product',readonly=True),
            'product_id17':fields.many2one('product.product','Product',readonly=True),
            'product_id18':fields.many2one('product.product','Product',readonly=True),
            'product_id19':fields.many2one('product.product','Product',readonly=True),
            'product_id20':fields.many2one('product.product','Product',readonly=True),
            'move_id1':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id2':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id3':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id4':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id5':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id6':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id7':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id8':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id9':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id10':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id11':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id12':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id13':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id14':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id15':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id16':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id17':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id18':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id19':fields.many2one('stock.move','Stock Move',readonly=True),
            'move_id20':fields.many2one('stock.move','Stock Move',readonly=True),
            'serialize_ids1':fields.many2many('product.serialize','picking_serialize_rel1','serial_id1','picking_id1','Serial No.'),
            'serialize_ids2':fields.many2many('product.serialize','picking_serialize_rel2','serial_id2','picking_id2','Serial No.'),
            'serialize_ids3':fields.many2many('product.serialize','picking_serialize_rel3','serial_id3','picking_id3','Serial No.'),
            'serialize_ids4':fields.many2many('product.serialize','picking_serialize_rel4','serial_id4','picking_id4','Serial No.'),
            'serialize_ids5':fields.many2many('product.serialize','picking_serialize_rel5','serial_id5','picking_id5','Serial No.'),
            'serialize_ids6':fields.many2many('product.serialize','picking_serialize_rel6','serial_id6','picking_id6','Serial No.'),
            'serialize_ids7':fields.many2many('product.serialize','picking_serialize_rel7','serial_id7','picking_id7','Serial No.'),
            'serialize_ids8':fields.many2many('product.serialize','picking_serialize_rel8','serial_id8','picking_id8','Serial No.'),
            'serialize_ids9':fields.many2many('product.serialize','picking_serialize_rel9','serial_id9','picking_id9','Serial No.'),
            'serialize_ids10':fields.many2many('product.serialize','picking_serialize_rel10','serial_id10','picking_id10','Serial No.'),
            'serialize_ids11':fields.many2many('product.serialize','picking_serialize_rel11','serial_id11','picking_id11','Serial No.'),
            'serialize_ids12':fields.many2many('product.serialize','picking_serialize_rel12','serial_id12','picking_id12','Serial No.'),
            'serialize_ids13':fields.many2many('product.serialize','picking_serialize_rel13','serial_id13','picking_id13','Serial No.'),
            'serialize_ids14':fields.many2many('product.serialize','picking_serialize_rel14','serial_id14','picking_id14','Serial No.'),
            'serialize_ids15':fields.many2many('product.serialize','picking_serialize_rel15','serial_id15','picking_id15','Serial No.'),
            'serialize_ids16':fields.many2many('product.serialize','picking_serialize_rel16','serial_id16','picking_id16','Serial No.'),
            'serialize_ids17':fields.many2many('product.serialize','picking_serialize_rel17','serial_id17','picking_id17','Serial No.'),
            'serialize_ids18':fields.many2many('product.serialize','picking_serialize_rel18','serial_id18','picking_id18','Serial No.'),
            'serialize_ids19':fields.many2many('product.serialize','picking_serialize_rel19','serial_id19','picking_id19','Serial No.'),
            'serialize_ids20':fields.many2many('product.serialize','picking_serialize_rel20','serial_id20','picking_id20','Serial No.'),
            
        }
    
    def view_init(self, cr , uid , fields_list, context=None):
        if context is None:
            context = {}
        incm_id = context.get('active_ids', False)
        for rec in self.pool.get('stock.partial.picking').browse(cr, uid, incm_id):
            i = 1
            for line in rec.move_ids:
                if line.product_id.serialized:
                    i+=1
                if i > 20:
                    raise osv.except_osv(_('Warning'), _('At one time you can only serialize 20 products. !'))
            pass
    
    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        result = super(picking_serialized_product, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
        if view_type == "form":
            incm_id = context.get('active_ids', False)
            doc = etree.XML(result['arch'])
            
            _moves_fields = result['fields']
            _moves_arch_lst = """
                                <form string="Picking Serialize Products" version="7.0">
                               """
            for rec in self.pool.get('stock.partial.picking').browse(cr, uid, incm_id):
                
                i = 1
                for line in rec.move_ids:
                    serial_id = []
                    if line.product_id.serialized:
                        for serial in line.move_id.serialize_ids:
                            serial_id.append(serial.id)
                        _moves_arch_lst += """
                        <group col="4" colspan="4">
                        <separator string="Enter %s serial number for product %s" colspan="4"/>
                        <field name="serialize_ids%s" nolabel="1" colspan="4" domain="[('product_id','=',%s),('id','in',%s)]"/>
                        </group>""" % (line.quantity,line.product_id.name,i,line.product_id.id,serial_id)
                        
                        _moves_fields.update({
                        "serialize_ids%s"%(i) : {'string': 'Serial No. Line','type': 'many2many','relation':'product.serialize'},
                        "product_id%s"%(i) : {'string': 'Product','type': 'many2one','relation':'product.product','readonly':True},
                        "move_id%s"%(i) : {'string': 'Stock Move','type': 'many2one','relation':'stock','readonly':True},
                        "qty%s"%(i) : {'string': 'Quantity','type': 'float','readonly':True},                
                        })
                        
                        _moves_arch_lst += """
                                            <newline/>
                                            """
                        i+=1
            
            _moves_arch_lst +="""<separator colspan="4"/>
                                   <group col="4" colspan="4">
                                   <button special="cancel" icon="gtk-cancel" string="Cancel" />
                                   <button name="picking_product" icon="gtk-ok" string="Approved1" type="object"/>
                                   </group>
                                </form>
                                """
            result['arch'] = _moves_arch_lst
            result['fields'] = _moves_fields
      
        return result
    
   
    
    def default_get(self, cr, uid, fields, context=None):
        res={}
        if not context:
            return res
        incm_id = context.get('active_ids', [])
        res = super(picking_serialized_product, self).default_get(cr, uid, fields, context=context)
        product_line = []
        if incm_id:
            for rec in self.pool.get('stock.partial.picking').browse(cr, uid, incm_id):
                i = 1
                for line in rec.move_ids:
                    if line.product_id.serialized:
                        if 'product_id%s'%(i) in fields:
                            res.update({'product_id%s'%(i) : line.product_id.id})
                        if 'move_id%s'%(i) in fields:
                            res.update({'move_id%s'%(i) : line.move_id.id})
                        if 'qty%s'%(i) in fields:
                            res.update({'qty%s'%(i) : line.quantity})
                        i+=1
                
                if 'name' in fields:
                    res.update({'name':time.strftime('%Y-%m-%d')})
          
        return res
    
    def picking_product(self, cr, uid, ids, context=None):
        if context is None: context = {}
        picking_ids = context.get('active_ids',[])
        context['picking_serialize_ids']=ids
        stock_obj = self.pool.get('stock.move')
        field = ['qty1','qty2','qty3','qty4','qty5','qty6','qty7','qty8','qty9','qty10','qty11','qty12','qty13','qty14','qty15','qty16','qty17','qty18','qty19','qty20',
                 'product_id1','product_id2','product_id3','product_id4','product_id5','product_id6','product_id7','product_id8','product_id9','product_id10',
                 'product_id11','product_id12','product_id13','product_id14','product_id15','product_id16','product_id17','product_id18','product_id19','product_id20',
                 'move_id1','move_id2','move_id3','move_id4','move_id5','move_id6','move_id7','move_id8','move_id9','move_id10','move_id11','move_id12','move_id13',
                 'move_id14','move_id15','move_id16','move_id17','move_id18','move_id19','move_id20','serialize_ids1','serialize_ids2','serialize_ids3','serialize_ids4','serialize_ids5',
                 'serialize_ids6','serialize_ids7','serialize_ids8','serialize_ids9','serialize_ids10','serialize_ids11','serialize_ids12','serialize_ids13','serialize_ids14','serialize_ids15','serialize_ids16',
                 'serialize_ids17','serialize_ids18','serialize_ids19','serialize_ids20',]
        serial_dict = {}
        for rec in self.read(cr, uid, ids, field):
            
            for i in range(1,21):
                if rec['product_id%s'%(i)] == False:
                    break
                if int(rec['qty%s'%(i)]) <> len(rec['serialize_ids%s'%(i)]):
                    raise osv.except_osv(('Warning !'),('Total quantity and number of serial lines doesnot match.' ))
            
                if rec['serialize_ids%s'%(i)]:
                    if serial_dict.has_key(rec['move_id%s'%(i)][0]):
                        serial_dict.update({str(rec['move_id%s'%(i)][0]):rec['serialize_ids%s'%(i)]})
                    else:
                        serial_dict[rec['move_id%s'%(i)][0]]=rec['serialize_ids%s'%(i)]
                    for id in rec['serialize_ids%s'%(i)]:
                        stock_obj.write(cr, uid, [rec['move_id%s'%(i)][0]],{'serialize_ids':[(3,id)]})
#                for line in self.pool.get('product.serialize').browse(cr, uid, rec['serialize_ids%s'%(i)]):
#                    if rec['product_id%s'%(i)] and rec['move_id%s'%(i)]:  
#                        print "======================================================================================="
#                        print cr.execute("update product_serialize set name = '"+str(line.name)+' return'+"' where product_id = '"+str(rec['product_id%s'%(i)][0])+"'")
#                        print "========================================================================================"          
#                        try:
##                            cr.execute("delete from product_serialize where product_id = '"+str(rec['product_id%s'%(i)][0])+"' and id = '"+str(line.id)+"'")
#                            
#                        except:
#                            raise osv.except_osv(('Invalid Operation !'),('Serial number '+ line.name +' cannot be returned, please check once again.' ))

        context['serial_dict']=serial_dict
        return self.pool.get('stock.partial.picking').do_partial(cr, uid, picking_ids, context=context)
#        return {'type': 'ir.actions.act_window_close'}

    
picking_serialized_product()