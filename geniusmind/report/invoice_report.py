import time
from openerp.report import report_sxw
from openerp.tools import amount_to_text_en
from openerp.tools.translate import _


class genius_delivery_challan(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(genius_delivery_challan, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'convert':self.convert,
                                  'get_serial':self.get_serial,
                                  })
        
    def convert(self, amount, cur):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
    def get_serial(self,line):
        result = ''
        if line:
            for val in line:
                result = result + " " + val.name
        return result
    
report_sxw.report_sxw('report.genius.delivery.challan', 'stock.picking', 'addons/geniusmind/report/delivery_challan.rml', parser=genius_delivery_challan)

class genius_purchase_order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(genius_purchase_order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'convert':self.convert,
                                  })
        
    def convert(self, amount, cur):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
report_sxw.report_sxw('report.genius.purchase.order', 'purchase.order', 'addons/geniusmind/report/purchase_order.rml', parser=genius_purchase_order)


class genius_sale_quotation(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(genius_sale_quotation, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'convert':self.convert,
                                  'calculate_price':self.calculate_price,
                                  })
        
    def convert(self, amount, cur):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
    def calculate_price(self, line):
        price = 0.0
        if line:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            
        return price
    
report_sxw.report_sxw('report.genius.sale.quotation', 'sale.order', 'addons/geniusmind/report/sale_quotation.rml', parser=genius_sale_quotation)

class genius_sale_order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(genius_sale_order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'convert':self.convert,
                                  'calculate_price':self.calculate_price,
                                  })
        
    def convert(self, amount, cur):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
    def calculate_price(self, line):
        price = 0.0
        if line:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
           
        return price
    
report_sxw.report_sxw('report.genius.sale.order', 'sale.order', 'addons/geniusmind/report/sale_order.rml', parser=genius_sale_order)

class genius_retail_invoice_delhi(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(genius_retail_invoice_delhi, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'convert':self.convert,
                                  'get_tax_percentage':self.get_tax_percentage,
                                  'get_serial':self.get_serial,
                                  })
        
    def convert(self, amount, cur):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
    def get_tax_percentage(self,line,name):
        percent = 0.0
        if not line:
            return 0.0
        for each in line:
            for tax in each.invoice_line_tax_id:
                if name and name == tax.name:
                   percent = tax.amount * 100
                
        return percent
    
    def get_serial(self,line):
        result = ''
        if line:
            for val in line:
                result = result + " " + val.name
       
        return result
    
report_sxw.report_sxw('report.genius.retail.invoice.delhi', 'account.invoice', 'addons/geniusmind/report/retail_invoice_delhi.rml', parser=genius_retail_invoice_delhi)




class genius_tax_invoice_delhi(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(genius_tax_invoice_delhi, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'convert':self.convert,
                                  'get_tax_percentage':self.get_tax_percentage,
                                  'get_serial':self.get_serial,
                                  })
        
    def convert(self, amount, cur):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
    def get_tax_percentage(self,line,name):
        percent = 0.0
        if not line:
            return 0.0
        for each in line:
            for tax in each.invoice_line_tax_id:
                if name and name == tax.name:
                   percent = tax.amount * 100
                
        return percent
    
    
    def get_serial(self,line):
        result = ''
        if line:
            for val in line:
                result = result + " " + val.name
        return result

report_sxw.report_sxw('report.genius.tax.invoice.delhi', 'account.invoice', 'addons/geniusmind/report/tax_invoice_delhi.rml', parser=genius_tax_invoice_delhi)


class genius_retail_invoice_bang(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(genius_retail_invoice_bang, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'convert':self.convert,
                                  'get_tax_percentage':self.get_tax_percentage,
                                  'get_serial':self.get_serial,
                                  })
        
    def convert(self, amount, cur):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
    def get_tax_percentage(self,line,name):
        percent = 0.0
        if not line:
            return 0.0
        for each in line:
            for tax in each.invoice_line_tax_id:
                if name and name == tax.name:
                   percent = tax.amount * 100
                
        return percent
    
    def get_serial(self,line):
        result = ''
        if line:
            for val in line:
                result = result + " " + val.name
        return result
    
report_sxw.report_sxw('report.genius.retail.invoice.bang', 'account.invoice', 'addons/geniusmind/report/retail_invoice_bang.rml', parser=genius_retail_invoice_bang)




class genius_tax_invoice_bang(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(genius_tax_invoice_bang, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'convert':self.convert,
                                  'get_tax_percentage':self.get_tax_percentage,
                                  'get_serial':self.get_serial,
                                  })
        
    def convert(self, amount, cur):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', cur)
        return amt_en
    
    def get_tax_percentage(self,line,name):
        percent = 0.0
        if not line:
            return 0.0
        for each in line:
            for tax in each.invoice_line_tax_id:
                if name and name == tax.name:
                   percent = tax.amount * 100
                
        return percent
    
    def get_serial(self,line):
        result = ''
        if line:
            for val in line:
                result = result + " " + val.name
        return result

report_sxw.report_sxw('report.genius.tax.invoice.bang', 'account.invoice', 'addons/geniusmind/report/tax_invoice_bang.rml', parser=genius_tax_invoice_bang)
