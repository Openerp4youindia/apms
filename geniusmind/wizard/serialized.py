from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from lxml import etree

class serialized_product(osv.osv_memory):
    _name = 'serialized.product'
 
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
            'line_ids1':fields.one2many('serialized.line1','serialized_id','Serial No. Line'),
            'line_ids2':fields.one2many('serialized.line2','serialized_id','Serial No. Line'),
            'line_ids3':fields.one2many('serialized.line3','serialized_id','Serial No. Line'),
            'line_ids4':fields.one2many('serialized.line4','serialized_id','Serial No. Line'),
            'line_ids5':fields.one2many('serialized.line5','serialized_id','Serial No. Line'),
            'line_ids6':fields.one2many('serialized.line6','serialized_id','Serial No. Line'),
            'line_ids7':fields.one2many('serialized.line7','serialized_id','Serial No. Line'),
            'line_ids8':fields.one2many('serialized.line8','serialized_id','Serial No. Line'),
            'line_ids9':fields.one2many('serialized.line9','serialized_id','Serial No. Line'),
            'line_ids10':fields.one2many('serialized.line10','serialized_id','Serial No. Line'),
            'line_ids11':fields.one2many('serialized.line11','serialized_id','Serial No. Line'),
            'line_ids12':fields.one2many('serialized.line12','serialized_id','Serial No. Line'),
            'line_ids13':fields.one2many('serialized.line13','serialized_id','Serial No. Line'),
            'line_ids14':fields.one2many('serialized.line14','serialized_id','Serial No. Line'),
            'line_ids15':fields.one2many('serialized.line15','serialized_id','Serial No. Line'),
            'line_ids16':fields.one2many('serialized.line16','serialized_id','Serial No. Line'),
            'line_ids17':fields.one2many('serialized.line17','serialized_id','Serial No. Line'),
            'line_ids18':fields.one2many('serialized.line18','serialized_id','Serial No. Line'),
            'line_ids19':fields.one2many('serialized.line19','serialized_id','Serial No. Line'),
            'line_ids20':fields.one2many('serialized.line20','serialized_id','Serial No. Line'),
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
        result = super(serialized_product, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
        if view_type == 'form':
            incm_id = context.get('active_ids', False)
            doc = etree.XML(result['arch'])
            _moves_fields = result['fields']
            _moves_arch_lst = """
                                <form string="Serializing Products" version="7.0">
                               """
            for rec in self.pool.get('stock.partial.picking').browse(cr, uid, incm_id):
                
                i = 1
                for line in rec.move_ids:
                    
                    if line.product_id.serialized:
                        _moves_arch_lst += """
                        <group col="4" colspan="4">
                        <separator string="Enter %s serial number for product %s" colspan="4"/>
                        <field name="line_ids%s" nolabel="1" colspan="4"/>
                        </group>""" % (line.quantity,line.product_id.name,i)
                    
                        _moves_fields.update({
                        "line_ids%s"%(i) : {'string': 'Serial No. Line','type': 'one2many','relation':'serialized.line%s'%(i)},
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
                                   <button name="return_do_partial" icon="gtk-ok" string="Approved" type="object"/>
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
        res = super(serialized_product, self).default_get(cr, uid, fields, context=context)
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
    
    def return_do_partial(self, cr, uid, ids, context=None):
        if context is None: context = {}
        picking_ids = context.get('active_ids',[])
        stock_obj = self.pool.get('stock.move')
        context['serial_wiz_id']=ids
        field = ['qty1','qty2','qty3','qty4','qty5','qty6','qty7','qty8','qty9','qty10','qty11','qty12','qty13','qty14','qty15','qty16','qty17','qty18','qty19','qty20',
                 'product_id1','product_id2','product_id3','product_id4','product_id5','product_id6','product_id7','product_id8','product_id9','product_id10',
                 'product_id11','product_id12','product_id13','product_id14','product_id15','product_id16','product_id17','product_id18','product_id19','product_id20',
                 'move_id1','move_id2','move_id3','move_id4','move_id5','move_id6','move_id7','move_id8','move_id9','move_id10','move_id11','move_id12','move_id13',
                 'move_id14','move_id15','move_id16','move_id17','move_id18','move_id19','move_id20','line_ids1','line_ids2','line_ids3','line_ids4','line_ids5',
                 'line_ids6','line_ids7','line_ids8','line_ids9','line_ids10','line_ids11','line_ids12','line_ids13','line_ids14','line_ids15','line_ids16',
                 'line_ids17','line_ids18','line_ids19','line_ids20',]
        for rec in self.read(cr, uid, ids, field):
            
            for i in range(1,21):
                if rec['product_id%s'%(i)] == False:
                    break
                if int(rec['qty%s'%(i)]) <> len(rec['line_ids%s'%(i)]):
                    raise osv.except_osv(('Warning !'),('Total quantity and number of serial lines doesnot match.' ))
           
                for line in self.pool.get('serialized.line%s'%(i)).browse(cr, uid, rec['line_ids%s'%(i)]):
                    if rec['product_id%s'%(i)] and rec['move_id%s'%(i)]:            
                        try:
                            serial_id = self.pool.get('product.serialize').search(cr, uid, [('product_id','=',rec['product_id%s'%(i)][0]),('name','=',line.serial_no)])
#                            stock_obj.write(cr, uid, [rec['move_id%s'%(i)][0]],{'serialize_ids':[(4,serial_id)]})
                            if serial_id:
                                raise osv.except_osv(('Duplicate key value violates unique constraint !'),('Serial number '+ line.serial_no +' is already exist, please enter unique serial number.' ))
                        except:
                            raise osv.except_osv(('Warning !'),('Provided information is not enough, Please check it again.'))
        context['serial_dict']={}     
        return self.pool.get('stock.partial.picking').do_partial(cr, uid, picking_ids, context=context)
#        return {'type': 'ir.actions.act_window_close'}

    
serialized_product()

class serialized_line1(osv.osv_memory):

    _name = 'serialized.line1'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line1()

class serialized_line2(osv.osv_memory):

    _name = 'serialized.line2'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line2()

class serialized_line3(osv.osv_memory):

    _name = 'serialized.line3'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line3()

class serialized_line4(osv.osv_memory):

    _name = 'serialized.line4'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line4()

class serialized_line5(osv.osv_memory):

    _name = 'serialized.line5'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line5()

class serialized_line6(osv.osv_memory):

    _name = 'serialized.line6'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line6()

class serialized_line7(osv.osv_memory):

    _name = 'serialized.line7'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line7()

class serialized_line8(osv.osv_memory):

    _name = 'serialized.line8'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line8()

class serialized_line9(osv.osv_memory):

    _name = 'serialized.line9'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line9()

class serialized_line10(osv.osv_memory):

    _name = 'serialized.line10'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line10()

class serialized_line11(osv.osv_memory):

    _name = 'serialized.line11'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line11()

class serialized_line12(osv.osv_memory):

    _name = 'serialized.line12'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line12()

class serialized_line13(osv.osv_memory):

    _name = 'serialized.line13'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line13()

class serialized_line14(osv.osv_memory):

    _name = 'serialized.line14'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line14()

class serialized_line15(osv.osv_memory):

    _name = 'serialized.line15'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line15()

class serialized_line16(osv.osv_memory):

    _name = 'serialized.line16'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line16()

class serialized_line17(osv.osv_memory):

    _name = 'serialized.line17'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line17()

class serialized_line18(osv.osv_memory):

    _name = 'serialized.line18'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line18()

class serialized_line19(osv.osv_memory):

    _name = 'serialized.line19'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line19()

class serialized_line20(osv.osv_memory):

    _name = 'serialized.line20'
 
    _columns = {
            'serial_no':fields.char('Serialized Number',size=64,required=True),
            'serialized_id':fields.many2one('serialized.product','Serial No',ondelete='cascade'),
        }
    
serialized_line20()

    

