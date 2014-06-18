
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


{
    "name": "Genious Mind",
    "version": "1.0",
    "depends": ["base","account_base","product","sale","stock","account","purchase","account_voucher"],
    "author": "Robin Bahadur",
    "category": "Custom",
    "description": """
    This module is custom module for serialized product, it provide functionality to serialize
    product, all purchasing, sales and invoice is done on the base of serial number.
    The inventory is also serialized. Two types of new journal define, Retail and Tax type journal.
    All module has its own report
    
    """,
    "init_xml": [],
    'update_xml': [
		   'report/report_view.xml',
           'views/invoice_view.xml',
                   'views/partner_view.xml',
                   'wizard/update_view.xml',
                   'views/product_view.xml',
                   'data/template.xml',
                   'views/mail_view.xml',
                   'views/sale_view.xml',
                   'views/purchase_view.xml',
                   'views/stock_view.xml',
                   'views/account_voucher_receipt_view.xml',
                   'wizard/shipping_view.xml',
                   'wizard/serialized_wizard_view.xml',
                   'wizard/partial_serialized_view.xml',
                   'wizard/return_serialized_wizard_view.xml',
                   'wizard/picking_serialized_wizard_view.xml',
                   'wizard/invoice_report_view.xml',
                   'security/ir.model.access.csv',
		           'data/invoice_data.xml',
                   
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}
