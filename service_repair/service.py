
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


from openerp.osv import osv
from openerp.osv import fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import time
from openerp.tools.translate import _

class order_type(osv.osv):
    _name = 'order.type'

    _columns = {
                'name':fields.char('Name',size=64,required=True),
                'address_id':fields.many2one('res.partner.address','Address',required=True)
                }

order_type()

class standard_problem(osv.osv):
    _name = 'standard.problem'

    _columns = {
                'name':fields.char('Name',size=64,required=True),
                'description':fields.text('Description',required=True),
                }

standard_problem()

class product_accessory(osv.osv):
    _name = 'product.accessory'
    
    _columns = {
                'name':fields.char('Name',size=64,required=True),
                'description':fields.text('Description'),
                }
    
product_accessory()

class standard_diagnosis(osv.osv):
    _name = 'standard.diagnosis'
    
    _columns = {
                'name':fields.char('Name',size=64,required=True),
                'description':fields.text('Description',required=True),
                }
    
standard_diagnosis()


class checklist_type(osv.osv):
    _name = 'checklist.type'
    
    _columns= {
               'name':fields.char('Name',size=64,required=True),
               'checklist_ids':fields.many2many('checklist.line','checklist_type_line_rel','line_id','type_id','Checklist Type'),
               }
checklist_type()    

class repair_order(osv.osv):
    _name = 'repair.order'
    
    SELECTION = [
                 ('draft','Draft'),
                 ('open','Open'),
                 ('diagnosis','Under Diagnosis'),
                 ('quote','DC-Quote Customer'),
                 ('purchase','DC-Order Part'),
                 ('ordered','Part Ordered'),
                 ('received','Part Received'),
                 ('reordered','Part Reordered'),
                 ('complete','Repair Complete'),
                 ('delivered','Delivered'),
                 ('calling','Happy Calling Done'),
                 ('return','Return Without Repair'),
                 ('cancel','Cancel'),
                 ]
    
    def _calculate_amount(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_total': 0.0,
            }
            val1 = 0.0
            for line in order.spare_line:
               val1 += line.price_subtotal
            res[order.id]['amount_total']=round(val1,2)
        return res
    
 
    _columns = {
            'type_id':fields.many2one('order.type','Type',required=True,readonly=True,states={'draft':[('readonly',False)]}),
            'name':fields.char('Reference', size=64,readonly=True),
            'partner_id':fields.many2one('res.partner','Customer',required=True,readonly=True,states={'draft':[('readonly',False)]}),
            'service_person_id':fields.many2one('res.users','Service Person'),
            'type':fields.selection([('warranty','Warranty'),('app','APP'),('chargeable','Chargeable'),('technical','Technical Support'),('physical','Physical Damage')],'Service Type',required=True, readonly=True,states={'draft':[('readonly',False)]}),
            'backup':fields.boolean('Data Backup',readonly=True,states={'draft':[('readonly',False)]}),
            'inward_date':fields.datetime('Machine Inward Date & Time',required=True,readonly=True,states={'draft':[('readonly',False)]}),
            'login_date':fields.datetime('GSX Repair Login Date & Time'),
            'close_date':fields.datetime('Repair Closed Date & Time'),
            'collect_date':fields.datetime('Machine Collection Date & Time'),
            'product_id':fields.many2one('product.product','Product',required=True,readonly=True,states={'draft':[('readonly',False)]}),
            'purchase_date':fields.date('Purchase Date'),
            'serial_no':fields.char('Serial Number',size=64),
            'problem_id':fields.many2one('standard.problem','Standard Problem'),
            'gsx_no':fields.char('GSX Repair Notification Number',size=64),
            'problem_desc':fields.text('Problem Description'),
            'picture1':fields.binary('Picture'),
            'picture2':fields.binary('Picture'),
            'picture3':fields.binary('Picture'),
            'equip_candition':fields.text('Equipment Candition'),
            'accessory_id':fields.many2many('product.accessory','order_accessory_rel','accessory_id','order_id','Accessories Received'),
            'upgrade':fields.text('Custom Upgrades'),
            'checklist_id':fields.many2one('checklist.type','Checklist Type'),
            'checklist_line':fields.one2many('checklist.item','order_id','Checklist Line'),
            'engineer_id1':fields.many2one('res.users','Engineer Assigned 1'),
            'engineer_id2':fields.many2one('res.users','Engineer Assigned 2'),
            'diagnosis_id':fields.many2one('standard.diagnosis','Standard Diagnosis',readonly=True,states={'draft':[('readonly',False)],'open':[('readonly',False)],'diagnosis':[('readonly',False)]}),
            'spare_line':fields.one2many('spare.product','order_id','Spares Replaced/Estimated Cost',readonly=True,states={'draft':[('readonly',False)],'open':[('readonly',False)],'diagnosis':[('readonly',False)],'quote':[('readonly',False)],'reordered':[('readonly',False)],'received':[('readonly',False)],'purchase':[('readonly',False)],'ordered':[('readonly',False)]}),
            'part_reorder':fields.boolean('Parts Reordered'),
            'customer_happy':fields.boolean('Customer Un-Happy/Un-Satisfied'),
            'customer_neutral':fields.boolean('Customer Neutral'),
            'machine_collected':fields.boolean('Machine Collected BY Customer'),
            'diagnosis_result':fields.text('Diagnosis Result'),
            'work_done':fields.text('Work Done'),
            'calling':fields.text('Happy Calling'),
            'internal_note':fields.text('Internal Notes'),
            'printed_note':fields.text('Printed Notes'),
            'state':fields.selection(SELECTION,'Status',readonly=True),
            'amount_total': fields.function(_calculate_amount, digits=(16,2),type="float", multi='sums',method=True,string='Total Amount',store=True),
        }
    
    _defaults = {
                 'state':'draft',
                 'inward_date':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                 'service_person_id': lambda self,cr,uid, ctx: uid,
                 }
    
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        order = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for t in order:
            if t['state'] in ('draft', 'cancel'):
                unlink_ids.append(t['id'])
            else:
                raise osv.except_osv(_('Invalid action !'), _('You can only delete an order which is in draft or cancel state.'))
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True
    
    def state_open(self,cr,uid,ids):
        for rec in self.browse(cr,uid,ids):
            if not rec.name:
                name = self.pool.get('ir.sequence').get(cr,uid,'repair.order')
                self.write(cr,uid,ids,{'state':'open','name':name})
            else:
                self.write(cr,uid,ids,{'state':'open'})
        return True
    
    def service_diagnosis(self,cr,uid,ids):
        for rec in self.browse(cr,uid,ids):
            if rec.type in ['blank','warranty','app','chargeable','physical']:
                if not rec.engineer_id1:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Engineer Assigned 1.'))
                return True
            else:
                return False

    def state_diagnosis(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'diagnosis'})
        return True
    
    def state_complete(self,cr,uid,ids):
        for rec in self.browse(cr,uid,ids):
            for line in rec.spare_line:
                if not line.newserial_no:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter New Serial Number, for Product %s') %(line.name.name,))
                if not line.oldserial_no:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Old Serial Number, for Product %s') %(line.name.name,))
                if not line.newserial_no and not line.oldserial_no:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter New Serial Number and Old Serial Number, for Product %s') %(line.name.name,))
        self.write(cr,uid,ids,{'state':'complete'})
        return True
    
    def service_quote_cust(self,cr,uid,ids):
        for rec in self.browse(cr,uid,ids):
           if rec.backup==True:
               return True
           elif not rec.backup and rec.type in ['blank','chargeable','physical']:
               return True
           elif not rec.backup and rec.type in ['warranty','app']:
               return False
    
    def state_quote_cust(self,cr,uid,ids):
        for rec in self.browse(cr,uid,ids):
            if not rec.diagnosis_id:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Standard Diagnosis.'))
            self.write(cr,uid,ids,{'state':'quote'})
        return True
      
    def state_order_part(self,cr,uid,ids):
        for rec in self.browse(cr,uid,ids):
            if not rec.spare_line and not rec.diagnosis_id:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Standard Diagnosis and Spares Replaced.'))
            if not rec.spare_line:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Spares Replaced.'))
            if not rec.diagnosis_id:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Standard Diagnosis.'))
            status = False
            for line in rec.spare_line:
                if line.state == 'Approved':
                    status = True
            if not status:
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter atleast one Spares Product with Approved Status.'))
            self.write(cr,uid,ids,{'state':'purchase'})
        return True
        
    
    def state_parts_ordered(self,cr,uid,ids):
        for rec in self.browse(cr,uid,ids):
            if not rec.login_date and not rec.gsx_no:
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter GSX Repair Login Date & Time and GSX Repair Notification Number.'))
            if not rec.login_date:
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter GSX Repair Login Date & Time.'))
            if not rec.gsx_no:
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter GSX Repair Notification Number.'))
        self.write(cr,uid,ids,{'state':'ordered'})
        return True
    
    def state_received(self,cr,uid,ids,context=None):
        for rec in self.browse(cr,uid,ids):
            for line in rec.spare_line:
                if not line.newserial_no:
                    raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter New Serial Number, for Product %s') %(line.name.name,))
        self.write(cr,uid,ids,{'state':'received'})
        return True
 
    
    def service_reordered(self,cr,uid,ids,context=None):
        for rec in self.browse(cr,uid,ids):
            if rec.part_reorder==True:
                return True
            else:
                return False
            
    def state_reordered(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'reordered'})
        return True
 
    def state_delivered(self,cr,uid,ids,context=None):
        for rec in self.browse(cr,uid,ids):
            if not rec.close_date and rec.collect_date : 
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Repair Closed Date & Time and Machine Collection Date & Time.'))
            if not rec.close_date: 
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Repair Closed Date & Time.'))
            elif not rec.collect_date:
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Machine Collection Date & Time.'))
            self.write(cr,uid,ids,{'state':'delivered'})
        return True
 
 
    def state_happy_Calling(self,cr,uid,ids,context=None):
        for rec in self.browse(cr,uid,ids):
            if not rec.calling:
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Happy Calling Details.'))

            self.write(cr,uid,ids,{'state':'calling'})
        return True
 
    def return_without_repair(self, cr, uid, ids, context=None):
        res = {}
        for rec in self.browse(cr, uid, ids):
            if not rec.diagnosis_id:
                raise osv.except_osv(_('Invalid Information !'), _('To proceed to next step you must enter Standard Diagnosis.'))
            self.write(cr, uid, ids, {'state':'return'})
        return True
    

    def set_to_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'draft'})
        return True
    
    def create_invoice(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        if ids:
            res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
            res_id = res and res[1] or False,
    
            return {
                'name': _('Customer Invoices'),
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [res_id],
                'res_model': 'account.invoice',
                'context': "{'type':'out_invoice'}",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
            }
        else:
            return True
        
    def change_problem_id(self, cr, uid, ids, problem_id, context=None):
        res = {}
        res['value'] = {}
        if not problem_id:
            return {'value': {'problem_desc':False}}
        for rec in self.pool.get('standard.problem').browse(cr, uid, [problem_id]):
            res['value'] = {'problem_desc':rec.description or ''}
        return res
    
    def change_diagnosis_id(self, cr, uid, ids, diagnosis_id, context=None):
        res = {}
        res['value'] = {}
        if not diagnosis_id:
            return {'value': {'work_done':False}}
        for rec in self.pool.get('standard.diagnosis').browse(cr, uid, [diagnosis_id]):
            res['value'] = {'work_done':rec.description or ''}
        return res

    def _checklist(self, line):
        return (0,False,{'name':line.name,
                         'instate':line.instate,
                         'outstate':line.outstate,})
        
    def onchange_checklist(self, cr, uid, ids, checklist_id, context=None):
        res = {}
        res['value'] = {}
        check = []
        if not checklist_id:
            return {'value': {'checklist_line':False}}
        for rec in self.pool.get('checklist.type').browse(cr, uid, [checklist_id]):
            for line in rec.checklist_ids:
                check.append(self._checklist(line))
            res['value'] = {'checklist_line':check}
        return res
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state': 'draft',
            'name': False,
        })
        return super(repair_order, self).copy(cr, uid, id, default, context=context)
            
    
repair_order()

class spare_product(osv.osv):
    _name = 'spare.product'
    
    def _calculate_total(self, cr, uid, ids, name, arg, context=None):
        res = {}
        val = 0.0
        for rec in self.browse(cr, uid, ids, context=context):
            val = rec.quantity * rec.applicable_cost
            res[rec.id] = round(val,2)
        return res
    
    _columns = {
                'name':fields.many2one('product.product','Spare',required=True),
                'quantity':fields.float('Quantity',digits=(16,2),required=True),
                'unit_price':fields.float('Unit Price',digits=(16,2),required=True),
                'applicable_cost':fields.float('Applicable Cost',digits=(16,2),required=True),
                'oldserial_no':fields.char('Old Serial Number', size=64),
                'newserial_no':fields.char('New Serial Number', size=64),
                'serialize_ids':fields.many2many('product.serialize','spareproduct_serialize_rel','spare_id','serial_id','Serial No.'),
                'order_id':fields.many2one('repair.order','Repair order'),
                'state':fields.selection([('Not Approved','Not Approved'),('Approved','Approved')],'Status',required=True),
                
                'price_subtotal': fields.function(_calculate_total, string='Subtotal', digits=(16,2),store=True),
                }
    _defaults = {
                 'quantity':1.0,
                 'state':'Not Approved',
                 }
    
spare_product()

class checklist_line(osv.osv):
    _name = 'checklist.line'
    
    _columns = {
                'name':fields.char('Name',size=64,required=True),
                'instate':fields.selection([('Working','Working'),('Not Working','Not Working'),('Not Checked','Not Checked')],'Inward Status',required=True),
                'outstate':fields.selection([('Working','Working'),('Not Working','Not Working'),('Not Checked','Not Checked')],'Outward Status',required=True),

                }
    
    _defaults = {
                 'instate':'Not Working',
                 'outstate':'Not Working',
                 }
    
    
checklist_line()

class checklist_item(osv.osv):
    _name = 'checklist.item'
    
    _columns = {
                'name':fields.char('Name',size=64,required=True),
                'instate':fields.selection([('Working','Working'),('Not Working','Not Working'),('Not Checked','Not Checked')],'Inward Status',required=True),
                'outstate':fields.selection([('Working','Working'),('Not Working','Not Working'),('Not Checked','Not Checked')],'Outward Status',required=True),
                'order_id':fields.many2one('repair.order','Repair order'),
                }
    
    _defaults = {
                 'instate':'Not Working',
                 'outstate':'Not Working',
                 }
    
    
checklist_item()
