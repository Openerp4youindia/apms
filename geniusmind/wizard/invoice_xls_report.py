from openerp.osv import osv, fields
from openerp.tools.translate import _
import os
import base64, urllib

import time
import cStringIO
from xlwt import Workbook, XFStyle, Borders, Pattern, Font, Alignment,  easyxf


class Annexurea(osv.osv_memory):
    
     """   For Printing Excel Reports   """
     
     _name = "annexurea"
    
    
     def report_get(self,cr,uid,ids,context=None):
  
        this=self.browse(cr,uid,ids)
        
        #Define the font attributes for header
        fnt = Font()
        fnt.name = 'Arial'
        fnt.height= 275
        
        #Define the font attributes for header
        content_fnt = Font()
        content_fnt.name ='Arial'
        content_fnt.height =220
        align_content = Alignment()
        align_content.horz= Alignment.HORZ_LEFT
     
        borders = Borders()
        borders.left = 0x02
        borders.right = 0x02
        borders.top = 0x02
        borders.bottom = 0x02
        
        #The text should be centrally aligned
        align = Alignment()
        align.horz = Alignment.HORZ_LEFT
        align.vert = Alignment.VERT_TOP
        align.wrap = Alignment.WRAP_AT_RIGHT
        
        #The text should be right aligned
        align1 = Alignment()
        align1.horz = Alignment.HORZ_RIGHT
        align1.vert = Alignment.VERT_TOP
        align1.wrap = Alignment.WRAP_AT_RIGHT
        
        #The content should be left aligned
        align2 = Alignment()
        align2.horz = Alignment.HORZ_LEFT
        align2.vert = Alignment.VERT_TOP
        align2.wrap = Alignment.WRAP_AT_RIGHT
        
        #The content should be right aligned
        align3 = Alignment()
        align3.horz = Alignment.HORZ_RIGHT
        align3.vert = Alignment.VERT_TOP
        align3.wrap = Alignment.WRAP_AT_RIGHT
        
        #We set the backgroundcolour here
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour =  0x1F
        
        #We set the backgroundcolour here
        pattern1 = Pattern()
        pattern1.pattern = Pattern.SOLID_PATTERN
        pattern1.pattern_fore_colour =  0x17
        
        #We set the backgroundcolour here
        pattern2 = Pattern()
        pattern2.pattern = Pattern.SOLID_PATTERN
        pattern2.pattern_fore_colour =  0xFF
        
        #We set the backgroundcolour here
        pattern3 = Pattern()
        pattern3.pattern = Pattern.SOLID_PATTERN
        pattern3.pattern_fore_colour =  0xFF

        #apply the above settings to the row(0) header
        style_header= XFStyle()
        style_header.font= fnt
        style_header.pattern= pattern
        style_header.borders = borders
        style_header.alignment=align    
        
        #apply the above settings to the row(1) header
        style_header1= XFStyle()
        style_header1.font= fnt
        style_header1.pattern= pattern1
        style_header1.borders = borders
        style_header1.alignment=align1  
        
        #apply the above settings to the content
        style_content_left= XFStyle()
        style_content_left.font= fnt
        style_content_left.pattern= pattern2
        style_content_left.borders = borders
        style_content_left.alignment=align2 
        
        style_content_right= XFStyle()
        style_content_right.font= fnt
        style_content_right.pattern= pattern3
        style_content_right.borders = borders
        style_content_right.alignment=align3 
        
        
        style_content= XFStyle()
        style_content.alignment = align_content 
        style_content.font = content_fnt

        wb = Workbook()
        ws = wb.add_sheet("Sheet 1")
        ws.row(0).height=3500
        ws.write(0,0,"(CO1)",style_header)
        ws.col(0).width = 2000
        ws.write(0,1,"Month & Year (CO2)",style_header)
        ws.col(1).width = 4500
        ws.write(0,2,"Seller's TIN (CO3)",style_header)
        ws.col(2).width = 4500
        ws.write(0,3,"Seller's Name (CO4)",style_header)
        ws.col(3).width = 10000
        ws.write(0,4,"Import From Outside India (CO5)",style_header)
        ws.col(4).width = 4500
        ws.write(0,5,"High Seas Purchase (CO6)",style_header)
        ws.col(5).width = 4500
        ws.write(0,6,"Purchase From Exempted Units (CO7)",style_header)
        ws.col(6).width = 4500
        ws.write(0,7,"Purchase From Unregistered Dealer/Composition Dealer/Non-creditable Goods/Against Retails Invoices/Tax Free Goods (CO8)",style_header)
        ws.col(7).width = 4500
        ws.write(0,8,"Interstate Purchase Of Tax Exempted Goods (CO9)",style_header)
        ws.col(8).width = 4500
        ws.write(0,9,"Interstate Purchase-Capital Goods (C1O)",style_header)
        ws.col(9).width = 4500
        ws.write(0,10,"Interstate Purchase - C Form (C11)",style_header)
        ws.col(10).width = 4500
        ws.write(0,11,"Interstate Purchase - H Form (C12)",style_header)
        ws.col(11).width = 4500
        ws.write(0,12,"Interstate Purchase - C + Form E1/E2 (C13)",style_header)
        ws.col(12).width = 4500
        ws.write(0,13,"Interstate Purchase None (C14)",style_header)
        ws.col(13).width = 4500
        ws.write(0,14,"Branch Transfer (C15)",style_header)
        ws.col(14).width = 4500
        ws.write(0,15,"Consignment Transfer (C16)",style_header)
        ws.col(15).width = 4500
        ws.write(0,16,"Local Purchase Eligible-Capital Goods Rates Of Tax (C17)",style_header)
        ws.col(16).width = 4500
        ws.write(0,17,"Local Purchase Eligible-Capital Goods Purchase (C18)",style_header)
        ws.col(17).width = 4500
        ws.write(0,18,"Local Purchase Eligible-Capital Goods Input Tax (C19)",style_header)
        ws.col(18).width = 4500
        ws.write(0,19,"Local Purchase Eligible-Capital Goods Total Purchase (C20)",style_header)
        ws.col(19).width = 4500
        ws.write(0,20,"Type Of Purchase (C21)",style_header)
        ws.col(20).width = 4500
        ws.write(0,21,"Local Purchase Eligible-Capital Others Rate Of Tax (C22)",style_header)
        ws.col(21).width = 4500
        ws.write(0,22,"Local Purchase Eligible-Capital Others Purchase (C23)",style_header)
        ws.col(22).width = 4500
        ws.write(0,23,"Local Purchase Eligible-Capital Others Input Tax (C24)",style_header)
        ws.col(23).width = 4500
        ws.write(0,24,"Local Purchase Eligible-Capital Others Total Purchase (C25)",style_header)
        ws.col(24).width = 4500
        
        ws.row(1).height=400
        ws.write(1,0,"0",style_header1)
        ws.write(1,1,"0",style_header1)
        ws.write(1,2,"0",style_header1)
        ws.write(1,3,"",style_header1)
        ws.write(1,4,"0.00",style_header1)
        ws.write(1,5,"0.00",style_header1)
        ws.write(1,6,"0.00",style_header1)
        ws.write(1,7,"0.00",style_header1)
        ws.write(1,8,"0.00",style_header1)
        ws.write(1,9,"0.00",style_header1)
        ws.write(1,10,"0.00",style_header1)
        ws.write(1,11,"0.00",style_header1)
        ws.write(1,12,"0.00",style_header1)
        ws.write(1,13,"0.00",style_header1)
        ws.write(1,14,"0.00",style_header1)
        ws.write(1,15,"0.00",style_header1)
        ws.write(1,16,"0.00",style_header1)
        ws.write(1,17,"0.00",style_header1)
        ws.write(1,18,"0.00",style_header1)
        ws.write(1,19,"0.00",style_header1)
        ws.write(1,20,"",style_header1)
        ws.write(1,21,"0.00",style_header1)
        ws.write(1,22,"0.00",style_header1)
        ws.write(1,23,"0.00",style_header1)
        ws.write(1,24,"0.00",style_header1)
        
        inv_obj = self.pool.get('account.invoice')
        line_obj = self.pool.get('account.invoice.line')
        
        row = 2
        count = 1
        value = 0.0
        sum1=sum2=sum3=sum4=sum5=sum6=0.0
        period = []
        for each in this:
            if each.start_period_id.name > each.end_period_id.name:
                raise osv.except_osv(_('Warning !'),_("Start period must be less than end period !") )
            cr.execute("select id from account_period where name between '"+str(each.start_period_id.name)+"' and '"+str(each.end_period_id.name)+"'")
            temp = cr.fetchall()
            for val in temp:
                if val:
                    period.append(val[0])
            inv_ids = inv_obj.search(cr, uid, [('type','=','in_invoice'),('state', 'not in',['draft','cancel']),('period_id','in',period)])
            line_ids = line_obj.search(cr, uid, [('invoice_id', 'in',inv_ids)])
            for line in line_obj.browse(cr, uid, line_ids):
                ws.row(row).height=400
                ws.write(row,0,count,style_content_right)
                ws.write(row,1,line.invoice_id.period_id and line.invoice_id.period_id.name or False,style_content_right)
                ws.write(row,2,line.partner_id.tin_no or '',style_content_right)
                ws.write(row,3,line.partner_id.name,style_content_left)
                if line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.country_id and line.invoice_id.address_invoice_id.country_id.name != 'India' or line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.country_id and line.invoice_id.address_invoice_id.country_id.name.lower() != 'india':
                    ws.write(row,4,round(line.price_subtotal,2),style_content_right)
                if not line.partner_id.tin_no:
                    ws.write(row,7,round(line.price_subtotal,2),style_content_right)
                for tax in line.invoice_line_tax_id:
                    value = tax.amount * 100
                if line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.city and line.invoice_id.address_invoice_id.city.lower() == 'new delhi' or line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.city and line.invoice_id.address_invoice_id.city.lower() == 'delhi' or  line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.state_id and line.invoice_id.address_invoice_id.state_id.name.lower() == 'new delhi' or line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.state_id and line.invoice_id.address_invoice_id.state_id.name.lower() == 'delhi':
                    ws.write(row,21,round(value,2),style_content_right)
                    ws.write(row,22,round(line.price_subtotal,2),style_content_right)
                    sum4 += round(line.price_subtotal,2)
                    ws.write(row,23,round(line.price_subtotal * tax.amount,2) ,style_content_right)
                    sum5 += round(line.price_subtotal * tax.amount,2)
                    ws.write(row,24,round(line.price_subtotal + (line.price_subtotal * tax.amount),2),style_content_right)
                    sum6 += round(line.price_subtotal + (line.price_subtotal * tax.amount),2)

                
                row += 1
                count += 1
            row += 2
            ws.row(row).height=400
            ws.write(row,0,"",style_header1)
            ws.write(row,1,"",style_header1)
            ws.write(row,2,"",style_header1)
            ws.write(row,3,"",style_header1)
            ws.write(row,4,"",style_header1)
            ws.write(row,5,"",style_header1)
            ws.write(row,6,"",style_header1)
            ws.write(row,7,"",style_header1)
            ws.write(row,8,"",style_header1)
            ws.write(row,9,"",style_header1)
            ws.write(row,10,"",style_header1)
            ws.write(row,11,"",style_header1)
            ws.write(row,12,"",style_header1)
            ws.write(row,13,"",style_header1)
            ws.write(row,14,"",style_header1)
            ws.write(row,15,"",style_header1)
            ws.write(row,16,"",style_header1)
            ws.write(row,17,"",style_header1)
            ws.write(row,18,"",style_header1)
            ws.write(row,19,"",style_header1)
            ws.write(row,20,"",style_header1)
            ws.write(row,21,"",style_header1)
            ws.write(row,22,sum4,style_header1)
            ws.write(row,23,sum5,style_header1)
            ws.write(row,24,sum6,style_header1) 
            f = cStringIO.StringIO()
            wb.save(f)
            out=base64.encodestring(f.getvalue())
               
               
        return self.write(cr, uid, ids, {'data':out, 'name':'MARAnnexure2A.xls'}, context=context)
       
    
     _columns = {
                    'name':fields.char('Filename',size=128),
                    'data':fields.binary('Data'),
                    'start_period_id':fields.many2one('account.period','Starting Period',required=True),
                    'end_period_id':fields.many2one('account.period','Ending Period',required=True),
                }

Annexurea()    

class Annexureb(osv.osv_memory):
    
     """   For Printing Excel Reports   """
     
     _name = "annexureb"
    
    
     def report_get(self,cr,uid,ids,context=None):
  
        this=self.browse(cr,uid,ids)
        
        #Define the font attributes for header
        fnt = Font()
        fnt.name = 'Arial'
        fnt.height= 275
        
        #Define the font attributes for header
        content_fnt = Font()
        content_fnt.name ='Arial'
        content_fnt.height =220
        align_content = Alignment()
        align_content.horz= Alignment.HORZ_LEFT
     
        borders = Borders()
        borders.left = 0x02
        borders.right = 0x02
        borders.top = 0x02
        borders.bottom = 0x02
        
        #The text should be centrally aligned
        align = Alignment()
        align.horz = Alignment.HORZ_LEFT
        align.vert = Alignment.VERT_TOP
        align.wrap = Alignment.WRAP_AT_RIGHT
        
        #The text should be right aligned
        align1 = Alignment()
        align1.horz = Alignment.HORZ_RIGHT
        align1.vert = Alignment.VERT_TOP
        align1.wrap = Alignment.WRAP_AT_RIGHT
        
        #The content should be left aligned
        align2 = Alignment()
        align2.horz = Alignment.HORZ_LEFT
        align2.vert = Alignment.VERT_TOP
        align2.wrap = Alignment.WRAP_AT_RIGHT
        
        #The content should be right aligned
        align3 = Alignment()
        align3.horz = Alignment.HORZ_RIGHT
        align3.vert = Alignment.VERT_TOP
        align3.wrap = Alignment.WRAP_AT_RIGHT
        
        #We set the backgroundcolour here
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour =  0x1F
        
        #We set the backgroundcolour here
        pattern1 = Pattern()
        pattern1.pattern = Pattern.SOLID_PATTERN
        pattern1.pattern_fore_colour =  0x17
        
        #We set the backgroundcolour here
        pattern2 = Pattern()
        pattern2.pattern = Pattern.SOLID_PATTERN
        pattern2.pattern_fore_colour =  0xFF
        
        #We set the backgroundcolour here
        pattern3 = Pattern()
        pattern3.pattern = Pattern.SOLID_PATTERN
        pattern3.pattern_fore_colour =  0xFF

        #apply the above settings to the row(0) header
        style_header= XFStyle()
        style_header.font= fnt
        style_header.pattern= pattern
        style_header.borders = borders
        style_header.alignment=align    
        
        #apply the above settings to the row(1) header
        style_header1= XFStyle()
        style_header1.font= fnt
        style_header1.pattern= pattern1
        style_header1.borders = borders
        style_header1.alignment=align1  
        
        #apply the above settings to the content
        style_content_left= XFStyle()
        style_content_left.font= fnt
        style_content_left.pattern= pattern2
        style_content_left.borders = borders
        style_content_left.alignment=align2 
        
        style_content_right= XFStyle()
        style_content_right.font= fnt
        style_content_right.pattern= pattern3
        style_content_right.borders = borders
        style_content_right.alignment=align3 
        
        
        style_content= XFStyle()
        style_content.alignment = align_content 
        style_content.font = content_fnt

        wb = Workbook()
        ws = wb.add_sheet("Sheet 1")
        ws.row(0).height=3500
        ws.write(0,0,"(CO1)",style_header)
        ws.col(0).width = 2000
        ws.write(0,1,"Month & Year (CO2)",style_header)
        ws.col(1).width = 4500
        ws.write(0,2,"Buyer's TIN (CO3)",style_header)
        ws.col(2).width = 4500
        ws.write(0,3,"Buyer's Name (CO4)",style_header)
        ws.col(3).width = 10000
        ws.write(0,4,"Interstate Branch/Consignment Transfer (CO5)",style_header)
        ws.col(4).width = 4500
        ws.write(0,5,"Export Out Of India (CO6)",style_header)
        ws.col(5).width = 4500
        ws.write(0,6,"High Sea Sales (CO7)",style_header)
        ws.col(6).width = 4500
        ws.write(0,7,"ISS - Goods Type (CO8)",style_header)
        ws.col(7).width = 4500
        ws.write(0,8,"ISS - Form Type (I) (CO9)",style_header)
        ws.col(8).width = 4500
        ws.write(0,9,"ISS - Rate Of Tax (C1O)",style_header)
        ws.col(9).width = 4500
        ws.write(0,10,"ISS - Sales Price (Excluding CST) (C11)",style_header)
        ws.col(10).width = 4500 
        ws.write(0,11,"ISS - Central Sales Tax (C12)",style_header)
        ws.col(11).width = 4500
        ws.write(0,12,"ISS - Total (C13)",style_header)
        ws.col(12).width = 4500
        ws.write(0,13,"Local Sale - Type Of Sale (C14)",style_header)
        ws.col(13).width = 4500
        ws.write(0,14,"Local Sale - Rate Of Tax (C15)",style_header)
        ws.col(14).width = 4500
        ws.write(0,15,"Local Sale - Sale Price (Excluding VAT) (C16)",style_header)
        ws.col(15).width = 4500
        ws.write(0,16,"Local Sale - OutPut Tax (C17)",style_header)
        ws.col(16).width = 4500
        ws.write(0,17,"Local Sale - Total (Including VAT) (C18)",style_header)
        ws.col(17).width = 4500
        
        ws.row(1).height=400
        ws.write(1,0,"0",style_header1)
        ws.write(1,1,"0",style_header1)
        ws.write(1,2,"0",style_header1)
        ws.write(1,3,"",style_header1)
        ws.write(1,4,"0.00",style_header1)
        ws.write(1,5,"0.00",style_header1)
        ws.write(1,6,"0.00",style_header1)
        ws.write(1,7,"",style_header1)
        ws.write(1,8,"",style_header1)
        ws.write(1,9,"0.00",style_header1)
        ws.write(1,10,"0.00",style_header1)
        ws.write(1,11,"0.00" ,style_header1)
        ws.write(1,12,"0.00",style_header1)
        ws.write(1,13,"",style_header1)
        ws.write(1,14,"0.00",style_header1)
        ws.write(1,15,"0.00",style_header1)
        ws.write(1,16,"0.00" ,style_header1)
        ws.write(1,17,"0.00",style_header1)

        inv_obj = self.pool.get('account.invoice')
        line_obj = self.pool.get('account.invoice.line')
        
        row = 2
        count = 1
        value = 0.0
        sum1=sum2=sum3=sum4=sum5=sum6=0.0
        period=[]
        for each in this:
            if each.start_period_id.name > each.end_period_id.name:
                raise osv.except_osv(_('Warning !'),_("Start period must be less than end period !") )
            cr.execute("select id from account_period where name between '"+str(each.start_period_id.name)+"' and '"+str(each.end_period_id.name)+"'")
            temp = cr.fetchall()
            for val in temp:
                if val:
                    period.append(val[0])
            inv_ids = inv_obj.search(cr, uid, [('type','=','out_invoice'),('state', 'not in',['draft','cancel']),('period_id','in',period)])
            line_ids = line_obj.search(cr, uid, [('invoice_id', 'in',inv_ids)])
            for line in line_obj.browse(cr, uid, line_ids):
                ws.row(row).height=400
                ws.write(row,0,count,style_content_right)
                ws.write(row,1,line.invoice_id.period_id and line.invoice_id.period_id.name or False,style_content_right)
                ws.write(row,2,line.partner_id.tin_no or '',style_content_right)
                ws.write(row,3,line.partner_id.name,style_content_left)
                
                
                for tax in line.invoice_line_tax_id:
                    value = tax.amount * 100
                if line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.city and line.invoice_id.address_invoice_id.city.lower() == 'new delhi' or line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.city and line.invoice_id.address_invoice_id.city.lower() == 'delhi' or  line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.state_id and line.invoice_id.address_invoice_id.state_id.name.lower() == 'new delhi' or line.invoice_id.address_invoice_id and line.invoice_id.address_invoice_id.state_id and line.invoice_id.address_invoice_id.state_id.name.lower() == 'delhi':
                    ws.write(row,14,round(value,2),style_content_right)
                    ws.write(row,15,round(line.price_subtotal,2),style_content_right)
                    sum1 += round(line.price_subtotal,2)
                    ws.write(row,16,round(line.price_subtotal * tax.amount,2) ,style_content_right)
                    sum2 += round(line.price_subtotal * tax.amount,2)
                    ws.write(row,17,round(line.price_subtotal + (line.price_subtotal * tax.amount),2),style_content_right)
                    sum3 += round(line.price_subtotal + (line.price_subtotal * tax.amount),2)
                else:                
                    ws.write(row,9,round(value,2),style_content_right)
                    ws.write(row,10,round(line.price_subtotal,2),style_content_right)
                    sum4 += round(line.price_subtotal,2)
                    ws.write(row,11,round(line.price_subtotal * tax.amount,2) ,style_content_right)
                    sum5 += round(line.price_subtotal * tax.amount,2)
                    ws.write(row,12,round(line.price_subtotal + (line.price_subtotal * tax.amount),2),style_content_right)
                    sum6 += round(line.price_subtotal + (line.price_subtotal * tax.amount),2)
               
                row += 1
                count += 1
            row += 2
            ws.row(row).height=400
            ws.write(row,0,"",style_header1)
            ws.write(row,1,"",style_header1)
            ws.write(row,2,"",style_header1)
            ws.write(row,3,"",style_header1)
            ws.write(row,4,"",style_header1)
            ws.write(row,5,"",style_header1)
            ws.write(row,6,"",style_header1)
            ws.write(row,7,"",style_header1)
            ws.write(row,8,"",style_header1)
            ws.write(row,9,"",style_header1)
            ws.write(row,10,sum4,style_header1)
            ws.write(row,11,sum5 ,style_header1)
            ws.write(row,12,sum6,style_header1)
            ws.write(row,13,"",style_header1)
            ws.write(row,14,"",style_header1)
            ws.write(row,15,sum1,style_header1)
            ws.write(row,16,sum2 ,style_header1)
            ws.write(row,17,sum3,style_header1)
            
                   
            f = cStringIO.StringIO()
            wb.save(f)
            out=base64.encodestring(f.getvalue())
               
               
        return self.write(cr, uid, ids, {'data':out, 'name':'MARAnnexure2B.xls'}, context=context)
       
    
     _columns = {
                    'name':fields.char('Filename',size=128),
                    'data':fields.binary('Data'),
                    'start_period_id':fields.many2one('account.period','Starting Period',required=True),
                    'end_period_id':fields.many2one('account.period','Ending Period',required=True),
                }

Annexureb()    


