from openerp.osv import fields, osv
from openerp.tools.translate import _
import re

class product_product(osv.osv):
    _inherit = 'product.product'
 
    _columns = {
                'default_code' : fields.char('Product Code', size=64),
                'ean13': fields.char('EAN13', size=13),
                'serialized':fields.boolean('Serialized'),
                'serialize_ids':fields.one2many('product.serialize','product_id','Serial No.'),
                }
    _sql_constraints=[('unique_product_code','unique (default_code)','Product with this code already exist please enter unique code !.'),
                      ('unique_ean13_code','unique (ean13)','Product with this EAN13 number already exist please enter unique code !.'),
                      ]

    def _check_ean_key(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            try:
                int(product.ean13)
            except:
                return False
        return True
    
    _constraints = [(_check_ean_key, 'Error: Invalid ean code', ['ean13'])]


    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        ext_ids  = []
        if type(ids) is int:
            ext_ids = ids
            ids = []
            ids.append(ext_ids)
        if not len(ids):
            return []
        def _name_get(d):
            name = d.get('name','')
            code = d.get('default_code',False)
            if code:
                name = '[%s] %s' % (code,name)
            if d.get('variants'):
                name = name + ' - %s' % (d['variants'],)
            return (d['id'], name)

        partner_id = context.get('partner_id', False)

        result = []
        for product in self.browse(cr, user, ids, context=context):
            sellers = filter(lambda x: x.name.id == partner_id, product.seller_ids)
            if sellers:
                for s in sellers:
                    mydict = {
                              'id': product.id,
                              'name': s.product_name or product.name,
                              'default_code': s.product_code or product.default_code,
                              'variants': product.variants,
                              'ean13':product.ean13
                              }
                    result.append(_name_get(mydict))
            else:
                mydict = {
                          'id': product.id,
                          'name': product.name,
                          'default_code': product.default_code,
                          'variants': product.variants,
                          'ean13':product.ean13
                          }
                result.append(_name_get(mydict))
        return result

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name:
            ids = self.search(cr, user, [('default_code','=',name)]+ args, limit=limit, context=context)
            if not ids:
                ids = self.search(cr, user, [('ean13','=',name)]+ args, limit=limit, context=context)
                
            if not ids:
                # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
                # on a database with thousands of matching products, due to the huge merge+unique needed for the
                # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
                # Performing a quick memory merge of ids in Python will give much better performance
                ids = set()
                ids.update(self.search(cr, user, args + [('default_code',operator,name)], limit=limit, context=context))
                ids.update(self.search(cr, user, args + [('ean13',operator,name)], limit=limit, context=context))
                if len(ids) < limit:
                    # we may underrun the limit because of dupes in the results, that's fine
                    ids.update(self.search(cr, user, args + [('name',operator,name)], limit=(limit-len(ids)), context=context))
                ids = list(ids)
            if not ids:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    ids = self.search(cr, user, [('default_code','=', res.group(2))] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context={}

        if not default:
            default = {}

        # Craft our own `<name> (copy)` in en_US (self.copy_translation()
        # will do the other languages).
        context_wo_lang = context.copy()
        context_wo_lang.pop('lang', None)
        product = self.read(cr, uid, id, ['name','default_code','ean13'], context=context_wo_lang)
        default = default.copy()
        val = product['name']
        temp = new = 0
        temp1 = new1 = 0
        try:
            if not val.find('(copy') == -1:
                pos = val.find('(copy') - 1
                name = val[0:pos]
                cr.execute("select count(id) from product_template where name like '" +name+"%"+"'" )
                temp = cr.fetchone()[0]
                product['name'] = name + ' (copy-'+ str(temp) + ')'
            elif val.find('(copy') == -1:
                cr.execute("select count(id) from product_template where name like '" +val+"%"+"'" )
                temp = cr.fetchone()[0]
                product['name'] = val + ' (copy-'+ str(temp) + ')'
            else:
                product['name'] = val + ' (copy)'
        except:
            product['name'] = val + ' (copy)'
            
        val1 = product['default_code']
        try:
            if not val1.find('(copy') == -1:
                pos1 = val1.find('(copy') - 1
                code = val1[0:pos1]
                cr.execute("select count(id) from product_product where default_code like '" +code+"%"+"'" )
                temp1 = cr.fetchone()[0]
                product['default_code'] = code + ' (copy-'+ str(temp1) + ')'
            elif val1.find('(copy') == -1:
                cr.execute("select count(id) from product_product where default_code like '" +val1+"%"+"'" )
                temp1 = cr.fetchone()[0]
                product['default_code'] = val1 + ' (copy-'+ str(temp1) + ')'
            else:
                product['default_code'] = product['default_code'] + ' (copy)'
        except:
            product['default_code'] = product['default_code'] + ' (copy)'
        
        default['name'] = product['name']
        default['default_code'] = product['default_code']
        default['ean13'] = False
        default['serialize_ids'] = False
        if context.get('variant',False):
            fields = ['product_tmpl_id', 'active', 'variants',
                    'price_margin', 'price_extra']
            data = self.read(cr, uid, id, fields=fields, context=context)
            for f in fields:
                if f in default:
                    data[f] = default[f]
            data['product_tmpl_id'] = data.get('product_tmpl_id', False) \
                    and data['product_tmpl_id'][0]
            del data['id']
            return self.create(cr, uid, data)
        else:
            return super(product_product, self).copy(cr, uid, id, default=default,
                    context=context)


product_product()

class product_template(osv.osv):
    _name = "product.template"
    _inherit = "product.template"

    
    def default_get(self, cr, uid, fields_list, context=None):
        res = super(product_template, self).default_get(cr, uid, fields_list, context=context)
        if 'cost_method' in fields_list:
                res.update({
                    'cost_method':'average',
                })
        if 'type' in fields_list:
                res.update({
                    'type':'product'
                })
        return res

    _columns={
              'description': fields.text('Description',translate=True),
              
              }

    _defaults={
               'description':'Demo Description'
               }
product_template()

class product_serialize(osv.osv):
    _name="product.serialize"
    
    _columns={
              'product_id':fields.many2one('product.product','Product',required=True,ondelete="cascade"),
              'name':fields.char('Serial No.',size=64,required=True,readonly=True),
              'state':fields.boolean('Sold',readonly=True),
              'inventory_id':fields.many2one('stock.inventory.line','Inventory Line',ondelete="cascade"),
              }
    
    _defaults={
               'state':False,
               }
    
    _sql_constraints=[
                      ('unique_product_serial_number', 'UNIQUE (product_id, name)', 'Product with this serial number already exist please enter unique serial number. !.')
                      ]

    def unlink(self, cr, uid, ids, context=None):
        serial = self.read(cr, uid, ids, ['name'], context=context)
        unlink_ids = []
        for s in serial:
            raise osv.except_osv(_('Invalid action !'), _('You cannot delete assigned serial number.'))

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)


product_serialize()


class product_inventory_serialize(osv.osv):
    _name="product.inventory.serialize"
    
    _columns={
              'name':fields.char('Serial No.',size=64,required=True),
              'prod_inv_id':fields.many2one('stock.inventory.line','Inventory Line',ondelete="cascade"),
              }
    
    
    _sql_constraints=[
                      ('unique_product_inventory_serial_number', 'UNIQUE (name)', 'Product with this serial number already exist please enter unique serial number. !.')
                      ]

product_inventory_serialize()
    
