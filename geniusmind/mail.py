import time
from openerp.osv import fields, osv
from openerp.tools.translate import _



class document_file(osv.osv):
    _inherit = 'ir.attachment'
    
    _columns = {
            'auto_attach': fields.boolean('Auto Attached to Mail'),
        }
    
#class mail_compose_message(osv.osv_memory):
#    _inherit = 'mail.compose.message'
#    
#    def on_change_template(self, cr, uid, ids, use_template, template_id, email_from=None, email_to=None, context=None):
#        if context is None:
#            context = {}
#        values = {}
#        if template_id:
#            res_id = context.get('mail.compose.target.id') or context.get('active_id') or False
#            if context.get('mail.compose.message.mode') == 'mass_mail':
#                # use the original template values - to be rendered when actually sent
#                # by super.send_mail()
#                values = self.pool.get('email.template').read(cr, uid, template_id, self.fields_get_keys(cr, uid), context)
#            else:
#                # render the mail as one-shot
#                values = self.pool.get('email.template').generate_email(cr, uid, template_id, res_id, context=context)
#                # retrofit generated attachments in the expected field format
#                if values['attachments']:
#                    attachment = values.pop('attachments')
#                    attachment_obj = self.pool.get('ir.attachment')
#                    att_ids = []
#                    for fname, fcontent in attachment.iteritems():
#                        data_attach = {
#                            'name': fname,
#                            'datas': fcontent,
#                            'datas_fname': fname,
#                            'description': fname,
#                            'res_model' : self._name,
#                            'res_id' : ids[0] if ids else False
#                        }
#                        att_ids.append(attachment_obj.create(cr, uid, data_attach))
#                    values['attachment_ids'] = att_ids
#                att = []
#                cr.execute("select id from ir_attachment where auto_attach = True limit 1")
#                temp = cr.fetchone()
#                if temp:
#                    for each in self.pool.get('ir.attachment').browse(cr, uid, [temp[0]], context):
#                        if values['attachment_ids']:
#                            att_ids.append(each.id)
#                            values['attachment_ids'] = att_ids
#                        else:
#                            att.append(each.id)
#                            values['attachment_ids'] = att
#        else:
#            # restore defaults
#            values = self.default_get(cr, uid, self.fields_get_keys(cr, uid), context)
#            values.update(use_template=use_template, template_id=template_id)
#
#        return {'value': values}
#
#    def default_get(self, cr, uid, fields, context=None):
#        if context is None:
#            context = {}
#        result = super(mail_compose_message, self).default_get(cr, uid, fields, context=context)
#        vals = {}
#        reply_mode = context.get('mail.compose.message.mode') == 'reply'
#        if (not reply_mode) and context.get('active_model') and context.get('active_id'):
#            # normal mode when sending an email related to any document, as specified by
#            # active_model and active_id in context
#            vals = self.get_value(cr, uid, context.get('active_model'), context.get('active_id'), context)
#        elif reply_mode and context.get('active_id'):
#            # reply mode, consider active_id is the ID of a mail.message to which we're
#            # replying
#            vals = self.get_message_data(cr, uid, int(context['active_id']), context)
#        else:
#            # default mode
#            result['model'] = context.get('active_model', False)
#        for field in vals:
#            if field in fields:
#                result.update({field : vals[field]})
#                
#        cr.execute("select id from ir_attachment where auto_attach = True limit 1")
#        temp = cr.fetchone()
#        if temp:
#            for each in self.pool.get('ir.attachment').browse(cr, uid, [temp[0]], context):
#                result.update({'attachment_ids' : [(6,0,[each.id])] })
#
#        # link to model and record if not done yet
#        if not result.get('model') or not result.get('res_id'):
#            active_model = context.get('active_model')
#            res_id = context.get('active_id')
#            if active_model and active_model not in (self._name, 'mail.message'):
#                result['model'] = active_model
#                if res_id:
#                    result['res_id'] = res_id
#
#        # Try to provide default email_from if not specified yet
#        if not result.get('email_from'):
#            current_user = self.pool.get('res.users').browse(cr, uid, uid, context)
#            result['email_from'] = current_user.user_email or False
#            
#        
#        return result