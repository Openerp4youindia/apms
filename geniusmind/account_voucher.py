from openerp.osv import fields, osv

class account_voucher(osv.osv):
    _inherit = "account.voucher"
    
    _columns = {
                'draft_cheque':fields.char('Draft/Cheque No',size=64),
                'bank':fields.char('Bank',size=64),
                'card_holder':fields.char('Card Holder',size=64),
                'card_number':fields.char('Card Number',size=64),
                'authorization':fields.char('Authorization',size=64),
                }

    
account_voucher()