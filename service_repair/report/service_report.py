import time
from openerp.report import report_sxw
from openerp.tools import amount_to_text_en
from openerp.osv import fields, osv
from openerp.tools.translate import _
from pytz import timezone


class service_order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(service_order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'timezone':timezone,
                                  'time':time,
                                  'convert':self.convert,
                                  'type':self.type,
                                  })
    
    def convert(self, amount, cur="Rupees"):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
    def type(self, val):
        result = 'Blank'
        if val and val == 'warranty':
            result = 'Warranty'
        elif val and val == 'app':
            result = 'APP'
        elif val and val == 'chargeable':
            result = 'Chargeable'
        elif val and val == 'technical':
            result = 'Technical Support'
        elif val and val == 'physical':
            result = 'Physical Damage'
        return result
    
report_sxw.report_sxw('report.service.order', 'repair.order', 'addons/service_repair/report/service_report.rml', parser=service_order)
