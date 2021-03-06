# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################
from openerp.osv import fields, osv

class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
        'vat_no' : fields.char('VAT Number', size=256),
        'cst_no' : fields.char('CST Number', size=256),
        'pan_no' : fields.char('PAN Number', size=256),
        'tin_no' : fields.char('TIN Number', size=256),
        'tan_no' : fields.char('TAN Number', size=256),
        'ser_tax': fields.char('Service Tax Number', size=256),
        'excise' : fields.char('Excise Number', size=256),
        'range'  : fields.char('Range', size=256),
        'div'    : fields.char('Division', size=256),
    }
    
    _sql_constraints=[('unique_tin_number','unique (tin_no)','Partner with this TIN Number already exist please enter unique number !.')]
