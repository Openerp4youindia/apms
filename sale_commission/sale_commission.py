from openerp.osv import fields, osv
import datetime
from openerp import tools

class sale_commission(osv.osv):
    
    _name = "sale.commission"
    
    _columns = {
#        "date":fields.date("Payment Date"),
        "user_id":fields.many2one("res.users", "Sale Person"),
#        "invoice_id":fields.many2one("account.invoice", "Customer Invoice"),
#        "product_id":fields.many2one("product.product", "Product"),
        "line_ids":fields.one2many("sale.commission.line", "commission_id", "Commission Lines")
    }
    
class sale_commission_line(osv.osv):
    
    _name = "sale.commission.line"
    
    _columns = {
        "commission_id":fields.many2one("sale.commission", "Commission"),
        "account_id":fields.many2one("account.analytic.account", "Customer Account"),
        "account_ref":fields.related("account_id", "code", type="char", string= "Acc No", size=32, relation="account.analytic.account"),
        "account_name":fields.related("account_id", "name", type="char", string= "Acc Name/Partner", size=128, relation="account.analytic.account"),
        "invoice_id":fields.many2one("account.invoice", "Customer Invoice"),
        "invoice_number":fields.related("invoice_id", "number", type="char", string= "Document Number", size=64, relation="account.invoice"),
        "invoice_type":fields.related("invoice_id", "type", type="selection",selection= [
            ('out_invoice','Customer Invoice'),
            ('in_invoice','Supplier Invoice'),
            ('out_refund','Customer Refund'),
            ('in_refund','Supplier Refund'),
            ],string= "Document Type", size=64, relation="account.invoice"),
        "related_document":fields.char("Related Document No", size=64),
        "invoice_date":fields.related("invoice_id", "invoice_date", type="date", string= "Document Creation Date", size=64, relation="account.invoice"),
        "statement_date":fields.date("Statement Date"),
        "recovery_days":fields.integer("Recovery Days"),
        "cost":fields.float("Cost"),
        "retail":fields.related("invoice_id", "amount_untaxed", type="float", string= "Retail", size=64, relation="account.invoice"),
        "vat":fields.float("VAT"),
        "gross_profit":fields.float("Gross Profit"),
        "payment_type":fields.char("Payment Type", size=64),
        "bank_charge":fields.float("Bank Charge"),
        "transport_cost":fields.float("Transport Cost"),
        "net_profit":fields.float("Net Profit"),
        "comission_payable":fields.float("Commission Payable"),
        "payment_late_by":fields.float("Payment Late By")
    }
class account_voucher(osv.osv):
    
    _inherit = "account.voucher"
    
    def button_proforma_voucher(self, cr, uid, ids, context=None):
        res = super(account_voucher, self).button_proforma_voucher(cr, uid, ids, context=context)
#        self.signal_proforma_voucher(cr, uid, ids)
        if context and context.get("invoice_id"):
            account_invoice_obj = self.pool.get("account.invoice")
            invoice_rec = account_invoice_obj.browse(cr, uid, context.get("invoice_id"), context= context)
            commission_obj = self.pool.get("sale.commission")
            commission_ids = commission_obj.search(cr, uid, [("user_id", '=', invoice_rec.user_id.id)], context = context)
            if commission_ids:
                commission_id = commission_ids[0]
            else:
                commission_id = commission_obj.create(cr, uid, {"user_id":invoice_rec.user_id.id}, context = context)
            for line in invoice_rec.invoice_line:
                value = {"user_id":invoice_rec.user_id.id, "invoice_id":invoice_rec.id, "product_id":line.product_id.id, "date":datetime.datetime.now().strftime(tools.DEFAULT_SERVER_DATE_FORMAT)}
                self.pool.get("sale.commission").create(cr, uid, value,context = context)
        return {'type': 'ir.actions.act_window_close'}