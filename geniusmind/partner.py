
from openerp.osv import fields, osv

class res_partner(osv.osv):
    _inherit = 'res.partner'
 
    _columns = {
                'reference_id': fields.many2one('res.partner','Reference'),
                'printed_note': fields.text('Printed Notes'),
                }
    _defaults = {
                 'user_id':lambda self, cr, uid, ctx:uid,
                 }
res_partner()

class res_partner_address(osv.osv):
    _description ='Partner Addresses'
    _name = 'res.partner.address'
    _order = 'type, name'
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner Name', ondelete='set null', select=True, help="Keep empty for a private address, not related to partner."),
        'type': fields.selection( [ ('default','Default'),('invoice','Invoice'), ('delivery','Delivery'), ('contact','Contact'), ('other','Other') ],'Address Type', help="Used to select automatically the right address according to the context in sales and purchases documents."),
        'function': fields.char('Function', size=128),
        'title': fields.many2one('res.partner.title','Title'),
        'name': fields.char('Contact Name', size=64, select=1),
        'street': fields.char('Street', size=128),
        'street2': fields.char('Street2', size=128),
        'zip': fields.char('Zip', change_default=True, size=24),
        'city': fields.char('City', size=128),
        'state_id': fields.many2one("res.country.state", 'Fed. State', domain="[('country_id','=',country_id)]"),
        'country_id': fields.many2one('res.country', 'Country'),
        'email': fields.char('E-Mail', size=240),
        'phone': fields.char('Phone', size=64),
        'fax': fields.char('Fax', size=64),
        'mobile': fields.char('Mobile', size=64),
        'phone2': fields.char('Phone 2', size=64),
        'birthdate': fields.char('Birthdate', size=64),
        'is_customer_add': fields.related('partner_id', 'customer', type='boolean', string='Customer'),
        'is_supplier_add': fields.related('partner_id', 'supplier', type='boolean', string='Supplier'),
        'active': fields.boolean('Active', help="Uncheck the active field to hide the contact."),
#        'company_id': fields.related('partner_id','company_id',type='many2one',relation='res.company',string='Company', store=True),
        'company_id': fields.many2one('res.company', 'Company',select=1),
        'color': fields.integer('Color Index'),
    }
    _defaults = {
        'active': lambda *a: 1,
        'company_id': lambda s,cr,uid,c: s.pool.get('res.company')._company_default_get(cr, uid, 'res.partner.address', context=c),
    }
    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if not len(ids):
            return []
        res = []
        for r in self.read(cr, user, ids, ['name','zip','country_id', 'city','partner_id', 'street']):
            if context.get('contact_display', 'contact')=='partner' and r['partner_id']:
                res.append((r['id'], r['partner_id'][1]))
            else:
                # make a comma-separated list with the following non-empty elements
                elems = [r['name'], r['country_id'] and r['country_id'][1], r['city'], r['street']]
                addr = ', '.join(filter(bool, elems))
                if (context.get('contact_display', 'contact')=='partner_address') and r['partner_id']:
                    res.append((r['id'], "%s: %s" % (r['partner_id'][1], addr or '/')))
                else:
                    res.append((r['id'], addr or '/'))
        return res

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}

        if not name:
            ids = self.search(cr, user, args, limit=limit, context=context)
        elif context.get('contact_display', 'contact') == 'partner':
            ids = self.search(cr, user, [('partner_id', operator, name)] + args, limit=limit, context=context)
        else:
            # first lookup zip code, as it is a common and efficient way to search on these data
            ids = self.search(cr, user, [('zip', '=', name)] + args, limit=limit, context=context)
            # then search on other fields:
            if context.get('contact_display', 'contact') == 'partner_address':
                fields = ['partner_id', 'name', 'country_id', 'city', 'street']
            else:
                fields = ['name', 'country_id', 'city', 'street']
            # Here we have to search the records that satisfy the domain:
            #       OR([[(f, operator, name)] for f in fields])) + args
            # Searching on such a domain can be dramatically inefficient, due to the expansion made
            # for field translations, and the handling of the disjunction by the DB engine itself.
            # So instead, we search field by field until the search limit is reached.
            while (not limit or len(ids) < limit) and fields:
                f = fields.pop(0)
                new_ids = self.search(cr, user, [(f, operator, name)] + args,
                                      limit=(limit-len(ids) if limit else limit),
                                      context=context)
                # extend ids with the ones in new_ids that are not in ids yet (and keep order)
                old_ids = set(ids)
                ids.extend([id for id in new_ids if id not in old_ids])

        if limit:
            ids = ids[:limit]
        return self.name_get(cr, user, ids, context=context)

    def get_city(self, cr, uid, id):
        return self.browse(cr, uid, id).city

    def _display_address(self, cr, uid, address, context=None):
        '''
        The purpose of this function is to build and return an address formatted accordingly to the
        standards of the country where it belongs.

        :param address: browse record of the res.partner.address to format
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''
        # get the address format
        address_format = address.country_id and address.country_id.address_format or \
                                         '%(street)s\n%(street2)s\n%(city)s,%(state_code)s %(zip)s' 
        # get the information that will be injected into the display format
        args = {
            'state_code': address.state_id and address.state_id.code or '',
            'state_name': address.state_id and address.state_id.name or '',
            'country_code': address.country_id and address.country_id.code or '',
            'country_name': address.country_id and address.country_id.name or '',
        }
        address_field = ['title', 'street', 'street2', 'zip', 'city']
        for field in address_field :
            args[field] = getattr(address, field) or ''

        return address_format % args

res_partner_address()

class shipping_zone(osv.osv):
    _name = 'shipping.zone'
    
    _columns = {
                'name':fields.char('Zone',size=64,required=True),
                'price':fields.float('Charges',digits=(16,2),required=True),
                
                }

shipping_zone()
