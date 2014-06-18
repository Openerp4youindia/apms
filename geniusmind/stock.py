import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc

class stock_return_picking(osv.osv_memory):
    _name = 'stock.return.picking'
    _inherit = 'stock.return.picking'
    
    def call_return_serialized(self, cr, uid, ids, context=None):
        res = {}
        serialize = False 
        if not context:
            context={}
        pick_obj = self.pool.get('stock.return.picking')
        picking_ids = context.get('active_ids', False)
        type = self.pool.get('stock.picking').browse(cr, uid, picking_ids[0]).type
        for pick in pick_obj.browse(cr, uid, ids, context=context):
            if type == 'in':
                for line in pick.product_return_moves:
                    if line.product_id and line.product_id.serialized:
                        serialize = True 
            
        if serialize:
            return {
                    'name':'Return Serialize Product',
                    'res_model':'return.serialized.product',
                    'type':'ir.actions.act_window',
                    'view_type':'form',
                    'view_mode':'form',
                    'target':'new',
                    'nodestroy': True,
                    'context': dict(context,active_ids=ids,picking=picking_ids)
                    }
        else:
            return self.create_returns(cr, uid, ids, context=context)
        
        
    def create_returns(self, cr, uid, ids, context=None):
        """ 
         Creates return picking.
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param ids: List of ids selected
         @param context: A standard dictionary
         @return: A dictionary which of fields with values.
        """
        if context is None:
            context = {} 
        record_id = context and context.get('active_id', False) or False
        return_ids = context and context.get('return_ids', False) or False
        move_obj = self.pool.get('stock.move')
        pick_obj = self.pool.get('stock.picking')
        uom_obj = self.pool.get('product.uom')
        data_obj = self.pool.get('stock.return.picking.memory')
        return_obj = self.pool.get('return.serialized.product')
        wf_service = netsvc.LocalService("workflow")
        pick = pick_obj.browse(cr, uid, record_id, context=context)
        data = self.read(cr, uid, ids[0], context=context)
        new_picking = None
        date_cur = time.strftime('%Y-%m-%d %H:%M:%S')
        set_invoice_state_to_none = True
        returned_lines = 0
        field = ['qty1','qty2','qty3','qty4','qty5','qty6','qty7','qty8','qty9','qty10','qty11','qty12','qty13','qty14','qty15','qty16','qty17','qty18','qty19','qty20',
                 'product_id1','product_id2','product_id3','product_id4','product_id5','product_id6','product_id7','product_id8','product_id9','product_id10',
                 'product_id11','product_id12','product_id13','product_id14','product_id15','product_id16','product_id17','product_id18','product_id19','product_id20',
                 'move_id1','move_id2','move_id3','move_id4','move_id5','move_id6','move_id7','move_id8','move_id9','move_id10','move_id11','move_id12','move_id13',
                 'move_id14','move_id15','move_id16','move_id17','move_id18','move_id19','move_id20','serialize_ids1','serialize_ids2','serialize_ids3','serialize_ids4','serialize_ids5',
                 'serialize_ids6','serialize_ids7','serialize_ids8','serialize_ids9','serialize_ids10','serialize_ids11','serialize_ids12','serialize_ids13','serialize_ids14','serialize_ids15','serialize_ids16',
                 'serialize_ids17','serialize_ids18','serialize_ids19','serialize_ids20',]
#        for rec in self.read(cr, uid, ids, field):
#            
#            for i in range(1,21):
#                if rec['product_id%s'%(i)] == False:
        
#        Create new picking for returned products
        if pick.type=='out':
            new_type = 'in'
        elif pick.type=='in':
            new_type = 'out'
        else:
            new_type = 'internal'
        new_picking = pick_obj.copy(cr, uid, pick.id, {'name':'%s-return' % pick.name,
                'move_lines':[], 'state':'draft', 'type':new_type,
                'date':date_cur, 'invoice_state':data['invoice_state'],'return_picking':True})
        
        val_id = data['product_return_moves']
        for v in val_id:
            data_get = data_obj.browse(cr, uid, v, context=context)
            mov_id = data_get.move_id.id
            new_qty = data_get.quantity
            move = move_obj.browse(cr, uid, mov_id, context=context)
            new_location = move.location_dest_id.id
            returned_qty = move.product_qty
            for rec in move.move_history_ids2:
                returned_qty -= rec.product_qty

            if returned_qty != new_qty:
                set_invoice_state_to_none = False
            if new_qty:
                returned_lines += 1
                serial = []
                if new_type == 'out':
                    if return_ids:
                        for rec in return_obj.read(cr, uid, return_ids, field):
                            for i in range(1,21):
                                if rec['product_id%s'%(i)] and rec['product_id%s'%(i)][0] == move.product_id.id and rec['move_id%s'%(i)] and rec['move_id%s'%(i)][0]==move.id:
                                    for val in rec['serialize_ids%s'%(i)]:
                                        serial.append(val)
                new_move=move_obj.copy(cr, uid, move.id, {
                    'product_qty': new_qty,
                    'product_uos_qty': uom_obj._compute_qty(cr, uid, move.product_uom.id,
                        new_qty, move.product_uos.id),
                    'picking_id':new_picking, 'state':'draft',
                    'location_id':new_location, 'location_dest_id':move.location_id.id,
                    'date':date_cur,
                    'serialize_ids':[(6,0,serial)]})
                move_obj.write(cr, uid, [move.id], {'move_history_ids2':[(4,new_move)]})
        if not returned_lines:
            raise osv.except_osv(_('Warning !'), _("Please specify at least one non-zero quantity!"))

        if set_invoice_state_to_none:
            pick_obj.write(cr, uid, [pick.id], {'invoice_state':'none'})
        wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_confirm', cr)
        pick_obj.force_assign(cr, uid, [new_picking], context)
        # Update view id in context, lp:702939
        view_list = {
                'out': 'view_picking_out_tree',
                'in': 'view_picking_in_tree',
                'internal': 'vpicktree',
            }
        data_obj = self.pool.get('ir.model.data')
        res = data_obj.get_object_reference(cr, uid, 'stock', view_list.get(new_type, 'vpicktree'))
        context.update({'view_id': res and res[1] or False})
        return {
            'domain': "[('id', 'in', ["+str(new_picking)+"])]",
            'name': 'Picking List',
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'stock.picking',
            'type':'ir.actions.act_window',
            'context':context,
        }
            
stock_return_picking()


class stock_partial_move(osv.osv_memory):
    _name = "stock.partial.move"
    _inherit = 'stock.partial.move'
    
    def call_partial_serialized(self, cr, uid, ids, context=None):
        res = {}
        serialize = False 
        if not context:
            context={}
        move_obj = self.pool.get('stock.move')
        move_id = context.get('active_ids', False)
        for move in move_obj.browse(cr, uid, move_id, context=context):
            if move.picking_id and move.picking_id.type == 'in' and not move.picking_id.sale_id:
                if move.product_id and move.product_id.serialized:
                    serialize = True 
                if serialize:
                    return {
                            'name':'Serializing Product',
                            'res_model':'partial.serialized.product',
                            'type':'ir.actions.act_window',
                            'view_type':'form',
                            'view_mode':'form',
                            'target':'new',
                            'nodestroy': True,
                            'context': dict(context,active_ids=ids,move=move_id)
                            }
                else:
                    return self.do_partial(cr, uid, ids, context=context)
            else:
#            context = dict(context,active_ids=ids,picking=picking_ids)
                return self.do_partial(cr, uid, ids, context=context)
    
stock_partial_move()

class stock_picking(osv.osv):
    _name = "stock.picking"
    _inherit = 'stock.picking'
    
 
    _columns = {
            'printed_note': fields.text('Printed Notes'),
            'return_picking':fields.boolean('Return Picking'),
            }
    
    _defaults={
               'return_picking':False,
               }
    
    def action_process(self, cr, uid, ids, context=None):
        if context is None: context = {}
        context = dict(context, active_ids=ids, active_model=self._name)
        for pick in self.browse(cr, uid, ids):
            if pick.type == 'out':
                for line in pick.move_lines:
                    if line.product_id and line.product_id.serialized:
                        if line.product_id and int(line.product_qty) <> len(line.serialize_ids):
                            raise osv.except_osv(('Warning !'),('Total quantity %s and number of serial lines %s doesnot match for product %s.' )%(int(line.product_qty), len(line.serialize_ids), line.product_id.name))
        partial_id = self.pool.get("stock.partial.picking").create(cr, uid, {}, context=context)
        return {
            'name':_("Products to Process"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'stock.partial.picking',
            'res_id': partial_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': context,
        }
    
    def action_assign(self, cr, uid, ids, *args):
        """ Changes state of picking to available if all moves are confirmed.
        @return: True
        """
        for pick in self.browse(cr, uid, ids):
            for line in pick.move_lines:
                if pick.type == 'out':
                    for line in pick.move_lines:
                        if line.product_id and line.product_id.serialized:
                            if line.product_id and int(line.product_qty) <> len(line.serialize_ids):
                                raise osv.except_osv(('Warning !'),('Either total quantity %s and number of serial lines %s doesnot match for product %s. or invoice is not created for this delivery.!' )%(int(line.product_qty), len(line.serialize_ids), line.product_id.name))
            move_ids = [x.id for x in pick.move_lines if x.state == 'confirmed']
            if not move_ids:
                raise osv.except_osv(_('Warning !'),_('Not enough stock, unable to reserve the products.'))
            self.pool.get('stock.move').action_assign(cr, uid, move_ids)
        return True

    def force_assign(self, cr, uid, ids, *args):
        """ Changes state of picking to available if moves are confirmed or waiting.
        @return: True
        """
        wf_service = netsvc.LocalService("workflow")
        for pick in self.browse(cr, uid, ids):
            for line in pick.move_lines:
                if pick.type == 'out':
                    for line in pick.move_lines:
                        if line.product_id and line.product_id.serialized:
                            if line.product_id and int(line.product_qty) <> len(line.serialize_ids):
                                raise osv.except_osv(('Warning !'),('Either total quantity %s and number of serial lines %s doesnot match for product %s. or invoice is not created for this delivery.!')%(int(line.product_qty), len(line.serialize_ids), line.product_id.name))
            move_ids = [x.id for x in pick.move_lines if x.state in ['confirmed','waiting']]
            self.pool.get('stock.move').force_assign(cr, uid, move_ids)
            wf_service.trg_write(uid, 'stock.picking', pick.id, cr)
        return True

    def draft_force_assign(self, cr, uid, ids, *args):
        """ Confirms picking directly from draft state.
        @return: True
        """
        wf_service = netsvc.LocalService("workflow")
        for pick in self.browse(cr, uid, ids):
            if not pick.move_lines:
                raise osv.except_osv(_('Error !'),_('You can not process picking without stock moves'))
            for line in pick.move_lines:
                if pick.type == 'out':
                    for line in pick.move_lines:
                        if line.product_id and line.product_id.serialized:
                            if line.product_id and int(line.product_qty) <> len(line.serialize_ids):
                                raise osv.except_osv(('Warning !'),('Either total quantity %s and number of serial lines %s doesnot match for product %s. or invoice is not created for this delivery.!' )%(int(line.product_qty), len(line.serialize_ids), line.product_id.name))
            wf_service.trg_validate(uid, 'stock.picking', pick.id,
                'button_confirm', cr)
        return True

    def draft_validate(self, cr, uid, ids, context=None):
        """ Validates picking directly from draft state.
        @return: True
        """
        wf_service = netsvc.LocalService("workflow")
        self.draft_force_assign(cr, uid, ids)
        for pick in self.browse(cr, uid, ids, context=context):
            for line in pick.move_lines:
                if pick.type == 'out':
                    for line in pick.move_lines:
                        if line.product_id and line.product_id.serialized:
                            if line.product_id and int(line.product_qty) <> len(line.serialize_ids):
                                raise osv.except_osv(('Warning !'),('Either total quantity %s and number of serial lines %s doesnot match for product %s. or invoice is not created for this delivery.!' )%(int(line.product_qty), len(line.serialize_ids), line.product_id.name))
            move_ids = [x.id for x in pick.move_lines]
            self.pool.get('stock.move').force_assign(cr, uid, move_ids)
            wf_service.trg_write(uid, 'stock.picking', pick.id, cr)
        return self.action_process(
            cr, uid, ids, context=context)
        
        
    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        """ Makes partial picking and moves done.
        @param partial_datas : Dictionary containing details of partial picking
                          like partner_id, address_id, delivery_date,
                          delivery moves with product_id, product_qty, uom
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        else:
            context = dict(context)
        res = {}
        serial_id = context.get('serial_wiz_id',[])
        move_obj = self.pool.get('stock.move')
        serial_obj = self.pool.get('serialized.product')
        product_obj = self.pool.get('product.product')
        currency_obj = self.pool.get('res.currency')
        uom_obj = self.pool.get('product.uom')
        sequence_obj = self.pool.get('ir.sequence')
        wf_service = netsvc.LocalService("workflow")
        serial_dict = context.get('serial_dict',{})
        serial_key = []
        serial_key1 = []
        for pick in self.browse(cr, uid, ids, context=context):
            new_picking = None
            complete, too_many, too_few = [], [], []
            move_product_qty, prodlot_ids, product_avail, partial_qty, product_uoms = {}, {}, {}, {}, {}
            
            field = ['qty1','qty2','qty3','qty4','qty5','qty6','qty7','qty8','qty9','qty10','qty11','qty12','qty13','qty14','qty15','qty16','qty17','qty18','qty19','qty20',
                 'product_id1','product_id2','product_id3','product_id4','product_id5','product_id6','product_id7','product_id8','product_id9','product_id10',
                 'product_id11','product_id12','product_id13','product_id14','product_id15','product_id16','product_id17','product_id18','product_id19','product_id20',
                 'move_id1','move_id2','move_id3','move_id4','move_id5','move_id6','move_id7','move_id8','move_id9','move_id10','move_id11','move_id12','move_id13',
                 'move_id14','move_id15','move_id16','move_id17','move_id18','move_id19','move_id20','line_ids1','line_ids2','line_ids3','line_ids4','line_ids5',
                 'line_ids6','line_ids7','line_ids8','line_ids9','line_ids10','line_ids11','line_ids12','line_ids13','line_ids14','line_ids15','line_ids16',
                 'line_ids17','line_ids18','line_ids19','line_ids20',]
            for rec in serial_obj.read(cr, uid, serial_id, field):
                
                for i in range(1,21):
                    if rec['product_id%s'%(i)] == False:
                        break
                    for line in self.pool.get('serialized.line%s'%(i)).browse(cr, uid, rec['line_ids%s'%(i)]):
                        if rec['product_id%s'%(i)] and rec['move_id%s'%(i)]:            
                            try:
                                serial_id = self.pool.get('product.serialize').create(cr, uid, {'product_id':rec['product_id%s'%(i)][0],'name':line.serial_no})
    #                            stock_obj.write(cr, uid, [rec['move_id%s'%(i)][0]],{'serialize_ids':[(4,serial_id)]})
                                if serial_id:
                                    if serial_dict.has_key(rec['move_id%s'%(i)][0]):
                                        serial_key.append(serial_id)
                                        serial_dict.update({str(rec['move_id%s'%(i)][0]):serial_key})
                                    else:
                                        serial_key = []
                                        serial_key.append(serial_id)
                                        serial_dict[rec['move_id%s'%(i)][0]]=serial_key
                                
                            except:
                                raise osv.except_osv(('Warning !'),('Provided information is not enough, Please check it again.'))
    
            for move in pick.move_lines:
                if move.state in ('done', 'cancel'):
                    continue
                partial_data = partial_datas.get('move%s'%(move.id), {})
                product_qty = partial_data.get('product_qty',0.0)
                move_product_qty[move.id] = product_qty
                product_uom = partial_data.get('product_uom',False)
                product_price = partial_data.get('product_price',0.0)
                product_currency = partial_data.get('product_currency',False)
                prodlot_id = partial_data.get('prodlot_id')
                prodlot_ids[move.id] = prodlot_id
                product_uoms[move.id] = product_uom
                partial_qty[move.id] = uom_obj._compute_qty(cr, uid, product_uoms[move.id], product_qty, move.product_uom.id)
                if move.product_qty == partial_qty[move.id]:
                    complete.append(move)
                elif move.product_qty > partial_qty[move.id]:
                    too_few.append(move)
                else:
                    too_many.append(move)

                # Average price computation
                if (pick.type == 'in') and (move.product_id.cost_method == 'average'):
                    product = product_obj.browse(cr, uid, move.product_id.id)
                    move_currency_id = move.company_id.currency_id.id
                    context['currency_id'] = move_currency_id
                    qty = uom_obj._compute_qty(cr, uid, product_uom, product_qty, product.uom_id.id)

                    if product.id in product_avail:
                        product_avail[product.id] += qty
                    else:
                        product_avail[product.id] = product.qty_available

                    if qty > 0:
                        new_price = currency_obj.compute(cr, uid, product_currency,
                                move_currency_id, product_price)
                        new_price = uom_obj._compute_price(cr, uid, product_uom, new_price,
                                product.uom_id.id)
                        if product.qty_available <= 0:
                            new_std_price = new_price
                        else:
                            # Get the standard price
                            amount_unit = product.price_get('standard_price', context=context)[product.id]
                            new_std_price = ((amount_unit * product_avail[product.id])\
                                + (new_price * qty))/(product_avail[product.id] + qty)
                        # Write the field according to price type field
                        product_obj.write(cr, uid, [product.id], {'standard_price': new_std_price})

                        # Record the values that were chosen in the wizard, so they can be
                        # used for inventory valuation if real-time valuation is enabled.
                        move_obj.write(cr, uid, [move.id],
                                {'price_unit': product_price,
                                 'price_currency_id': product_currency})


            for move in too_few:
                product_qty = move_product_qty[move.id]
                if not new_picking:
                    new_picking = self.copy(cr, uid, pick.id,
                            {
                                'name': sequence_obj.get(cr, uid, 'stock.picking.%s'%(pick.type)),
                                'move_lines' : [],
                                'state':'draft',
                            })
                if product_qty != 0:
                    defaults = {
                            'product_qty' : product_qty,
                            'product_uos_qty': product_qty, #TODO: put correct uos_qty
                            'picking_id' : new_picking,
                            'state': 'assigned',
                            'move_dest_id': False,
                            'price_unit': move.price_unit,
                            'product_uom': product_uoms[move.id],
                    }
                    prodlot_id = prodlot_ids[move.id]
                    if prodlot_id:
                        defaults.update(prodlot_id=prodlot_id)
                    if serial_dict.get(move.id):
                        defaults.update({'serialize_ids':[(6,0,serial_dict[move.id])]})
                    move_obj.copy(cr, uid, move.id, defaults)
                    
                move_obj.write(cr, uid, [move.id],
                        {
                            'product_qty' : move.product_qty - partial_qty[move.id],
                            'product_uos_qty': move.product_qty - partial_qty[move.id], #TODO: put correct uos_qty
                            
                        })

            if new_picking:
                move_obj.write(cr, uid, [c.id for c in complete], {'picking_id': new_picking})
            for move in complete:
                defaults = {'product_uom': product_uoms[move.id], 'product_qty': move_product_qty[move.id]}
                if prodlot_ids.get(move.id):
                    defaults.update({'prodlot_id': prodlot_ids[move.id]})
                if serial_dict.get(move.id):
                    defaults.update({'serialize_ids':[(6,0,serial_dict[move.id])]})
                move_obj.write(cr, uid, [move.id], defaults)
            for move in too_many:
                product_qty = move_product_qty[move.id]
                defaults = {
                    'product_qty' : product_qty,
                    'product_uos_qty': product_qty, #TODO: put correct uos_qty
                    'product_uom': product_uoms[move.id],
                }
                prodlot_id = prodlot_ids.get(move.id)
                if prodlot_ids.get(move.id):
                    defaults.update(prodlot_id=prodlot_id)
                if serial_dict.get(move.id):
                    defaults.update({'serialize_ids':[(6,0,serial_dict[move.id])]})
                if new_picking:
                    defaults.update(picking_id=new_picking)
                move_obj.write(cr, uid, [move.id], defaults)

            
            # At first we confirm the new picking (if necessary)
            if new_picking:
                wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_confirm', cr)
                # Then we finish the good picking
                self.write(cr, uid, [pick.id], {'backorder_id': new_picking})
                self.action_move(cr, uid, [new_picking])
                for new_pick in self.browse(cr, uid, [new_picking]):
                    if new_pick.return_picking:
                        for line in new_pick.move_lines:
                            for serial in line.serialize_ids:
                                move_obj.write(cr, uid,[line.id],{'serialize_ids':[(4,serial.id)]})
                                if new_pick.type == 'out':
                                    move_obj.write(cr, uid,[line.id],{'serialize_ids':[(4,serial.id)]})
                                    cr.execute("update product_serialize set name = 'R-"+str(serial.name)+"' where id=%s",(serial.id,))
                wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_done', cr)
                wf_service.trg_write(uid, 'stock.picking', pick.id, cr)
                delivered_pack_id = new_picking
            else:
                self.action_move(cr, uid, [pick.id])
                if pick.return_picking:
                    for line in pick.move_lines:
                        for serial in line.serialize_ids:
                            move_obj.write(cr, uid,[line.id],{'serialize_ids':[(4,serial.id)]})
                            if pick.type == 'out':
                                move_obj.write(cr, uid,[line.id],{'serialize_ids':[(4,serial.id)]})
                                cr.execute("update product_serialize set name = 'R-"+str(serial.name)+"' where id=%s",(serial.id,))
                wf_service.trg_validate(uid, 'stock.picking', pick.id, 'button_done', cr)
                delivered_pack_id = pick.id

            delivered_pack = self.browse(cr, uid, delivered_pack_id, context=context)
            res[pick.id] = {'delivered_picking': delivered_pack.id or False}

        return res
        
stock_picking()

class stock_partial_picking(osv.osv_memory):
    _inherit = "stock.partial.picking"
    def call_serialized(self, cr, uid, ids, context=None):
        res = {}
        serialize = False 
        uom_obj = self.pool.get('product.uom')
        if not context:
            context={}
        pick_obj = self.pool.get('stock.partial.picking')
        picking_ids = context.get('active_ids', False)
        for pick in pick_obj.browse(cr, uid, ids, context=context):
            if pick.picking_id and pick.picking_id.type == 'in' and not pick.picking_id.sale_id:
                for line in pick.move_ids:
                    if line.product_id and line.product_id.serialized:
                        serialize = True 
            if pick.picking_id and pick.picking_id.type == 'out':
                for move in pick.move_ids:
                    if move.product_id and move.product_id.serialized:
                        partial_qty = uom_obj._compute_qty(cr, uid, move.move_id.product_uom.id, move.quantity, move.product_uom.id)
                  
                        if move.move_id.product_qty > partial_qty:
                            return {
                                    'name':'Picking Serialize Product',
                                    'res_model':'picking.serialized.product',
                                    'type':'ir.actions.act_window',
                                    'view_type':'form',
                                    'view_mode':'form',
                                    'target':'new',
                                    'nodestroy': True,
                                    'context': dict(context,active_ids=ids,picking=picking_ids)
                                    }
                        if move.move_id.product_qty < partial_qty:
                            raise osv.except_osv(('Warning !'),('You cannot deliver order with quantity greater than actual quantity in move line'))
                        
                
            if serialize:
                return {
                        'name':'Serializing Product',
                        'res_model':'serialized.product',
                        'type':'ir.actions.act_window',
                        'view_type':'form',
                        'view_mode':'form',
                        'target':'new',
                        'nodestroy': True,
                        'context': dict(context,active_ids=ids,picking=picking_ids)
                        }
            else:
                return self.do_partial(cr, uid, ids, context=context)
        
#    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
#        result = super(stock_partial_picking, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
#
#        pick_obj = self.pool.get('stock.picking')
#        picking_ids = context.get('active_ids', False)
#
#        if not picking_ids:
#            # not called through an action (e.g. buildbot), return the default.
#            return result
#
#        for pick in pick_obj.browse(cr, uid, picking_ids, context=context):
#            picking_type = self.get_picking_type(cr, uid, pick, context=context)
#
#        _moves_arch_lst = """<form string="%s">
#                        <field name="date" invisible="1"/>
#                        <separator colspan="4" string="%s"/>
#                        <field name="%s" colspan="4" nolabel="1" mode="tree,form" width="550" height="200" ></field>
#                        """ % (_('Process Document'), _('Products'), "product_moves_" + picking_type)
#        _moves_fields = result['fields']
#
#        # add field related to picking type only
#        _moves_fields.update({
#                            'product_moves_' + picking_type: {'relation': 'stock.move.memory.'+picking_type, 'type' : 'one2many', 'string' : 'Product Moves'},
#                            })
#
#        _moves_arch_lst += """
#                <separator string="" colspan="4" />
#                <label string="" colspan="2"/>
#                <group col="2" colspan="2">
#                <button icon='gtk-cancel' special="cancel"
#                    string="_Cancel" />
#                <button name="call_serialized" string="_Serialize"
#                    colspan="1" type="object" icon="gtk-go-forward" />
#            </group>
#        </form>"""
#        result['arch'] = _moves_arch_lst
#        result['fields'] = _moves_fields
#        return result


stock_partial_picking()

class stock_move(osv.osv):
    _inherit = "stock.move"

    _columns={
              'serialize_ids':fields.many2many('product.serialize','stock_serialize_rel','serial_id','stock_id','Serial No.', states={'draft':[('readonly',False)]})
              }
    
    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False,
                            loc_dest_id=False, address_id=False):
        """ On change of product id, if finds UoM, UoS, quantity and UoS quantity.
        @param prod_id: Changed Product id
        @param loc_id: Source location id
        @param loc_id: Destination location id
        @param address_id: Address id of partner
        @return: Dictionary of values
        """
        warning = {}
        if not prod_id:
            return {}
        lang = False
        if address_id:
            addr_rec = self.pool.get('res.partner.address').browse(cr, uid, address_id)
            if addr_rec:
                lang = addr_rec.partner_id and addr_rec.partner_id.lang or False
        ctx = {'lang': lang}

        product = self.pool.get('product.product').browse(cr, uid, [prod_id], context=ctx)[0]
        uos_id  = product.uos_id and product.uos_id.id or False
        result = {
            'product_uom': product.uom_id.id,
            'product_uos': uos_id,
            'product_qty': 1.00,
            'product_uos_qty' : self.pool.get('stock.move').onchange_quantity(cr, uid, ids, prod_id, 1.00, product.uom_id.id, uos_id)['value']['product_uos_qty']
        }
        if not ids:
            result['name'] = product.partner_ref
        if loc_id:
            result['location_id'] = loc_id
        if loc_dest_id:
            result['location_dest_id'] = loc_dest_id
        if product.serialized:
            warning = {
                    'title': _('Serialize Information !'),
                    'message': _('You have selected a serialize product, Make sure to select serial number. !')
                    }
        return {'value': result, 'warning':warning}
    
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms stock move.
        @return: List of ids.
        """
#        for rec in self.browse(cr, uid, ids, context=context):
#            if rec.picking_id and rec.picking_id.type == 'out':
#                if rec.product_id and rec.product_id.serialized:
#                    if rec.product_id and int(rec.product_qty) <> len(rec.serialize_ids):
#                        raise osv.except_osv(('Warning !'),('Total quantity %s and number of serial lines %s doesnot match for product %s.' )%(int(rec.product_qty), len(rec.serialize_ids), rec.product_id.name))
        moves = self.browse(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'state': 'confirmed'})
        self.create_chained_picking(cr, uid, moves, context)
        return []

    def action_assign(self, cr, uid, ids, *args):
        """ Changes state to confirmed or waiting.
        @return: List of values
        """
        todo = []
        for move in self.browse(cr, uid, ids):
            if move.picking_id and move.picking_id.type == 'out':
                if move.product_id and move.product_id.serialized:
                    if move.product_id and int(move.product_qty) <> len(move.serialize_ids):
                        raise osv.except_osv(('Warning !'),('Either total quantity %s and number of serial lines %s doesnot match for product %s. or invoice is not created for this delivery.!' )%(int(move.product_qty), len(move.serialize_ids), move.product_id.name))
            if move.state in ('confirmed', 'waiting'):
                todo.append(move.id)
        res = self.check_assign(cr, uid, todo)
        return res

    def force_assign(self, cr, uid, ids, context=None):
        """ Changes the state to assigned.
        @return: True
        """
        for rec in self.browse(cr, uid, ids, context=context):
            if rec.picking_id and rec.picking_id.type == 'out':
                if rec.product_id and rec.product_id.serialized:
                    if rec.product_id and int(rec.product_qty) <> len(rec.serialize_ids):
                        raise osv.except_osv(('Warning !'),('Either total quantity %s and number of serial lines %s doesnot match for product %s. or invoice is not created for this delivery.!' )%(int(rec.product_qty), len(rec.serialize_ids), rec.product_id.name))
        self.write(cr, uid, ids, {'state': 'assigned'})
        return True


stock_move()

class stock_inventory(osv.osv):
    _inherit = "stock.inventory"

    def _inventory_line_hook(self, cr, uid, inventory_line, move_vals):
        """ Creates a stock move from an inventory line
        @param inventory_line:
        @param move_vals:
        @return:
        """
        return self.pool.get('stock.move').create(cr, uid, move_vals)

    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirm the inventory and writes its finished date
        @return: True
        """
        if context is None:
            context = {}
        # to perform the correct inventory corrections we need analyze stock location by
        # location, never recursively, so we use a special context
        product_context = dict(context, compute_child=False)

        location_obj = self.pool.get('stock.location')
        for inv in self.browse(cr, uid, ids, context=context):
            move_ids = []
            for line in inv.inventory_line_id:
                if line.product_id and line.product_id.serialized:
                    if line.product_id and int(line.product_qty) <> len(line.serial_line):
                        raise osv.except_osv(('Warning !'),('Total quantity %s and number of serial lines %s doesnot match for product %s.' )%(int(line.product_qty), len(line.serial_line), line.product_id.name))
                pid = line.product_id.id
                product_context.update(uom=line.product_uom.id, date=inv.date, prodlot_id=line.prod_lot_id.id)
                amount = location_obj._product_get(cr, uid, line.location_id.id, [pid], product_context)[pid]

                change = line.product_qty - amount
                lot_id = line.prod_lot_id.id
                if change:
                    location_id = line.product_id.product_tmpl_id.property_stock_inventory.id
                    value = {
                        'name': 'INV:' + str(line.inventory_id.id) + ':' + line.inventory_id.name,
                        'product_id': line.product_id.id,
                        'product_uom': line.product_uom.id,
                        'prodlot_id': lot_id,
                        'date': inv.date,
                    }
                    if change > 0:
                        value.update( {
                            'product_qty': change,
                            'location_id': location_id,
                            'location_dest_id': line.location_id.id,
                        })
                    else:
                        value.update( {
                            'product_qty': -change,
                            'location_id': line.location_id.id,
                            'location_dest_id': location_id,
                        })
                    move_ids.append(self._inventory_line_hook(cr, uid, line, value))
            message = _('Inventory') + " '" + inv.name + "' "+ _("is done.")
            self.log(cr, uid, inv.id, message)
            self.write(cr, uid, [inv.id], {'state': 'confirm', 'move_ids': [(6, 0, move_ids)]})
        return True
    
    def action_done(self, cr, uid, ids, context=None):
        """ Finish the inventory
        @return: True
        """
        if context is None:
            context = {}
        move_obj = self.pool.get('stock.move')
        for inv in self.browse(cr, uid, ids, context=context):
            move_obj.action_done(cr, uid, [x.id for x in inv.move_ids], context=context)
            self.write(cr, uid, [inv.id], {'state':'done', 'date_done': time.strftime('%Y-%m-%d %H:%M:%S')}, context=context)

            for line in inv.inventory_line_id:
                if line.product_id and line.product_id.serialized:
                    for serial in line.serial_line:
                        self.pool.get('product.serialize').create(cr, uid, {'product_id':line.product_id and line.product_id.id or False,'name':serial.name})
                        
        return True

stock_inventory()

class stock_inventory_line(osv.osv):
    _inherit = "stock.inventory.line"
    
    _columns={
              'serial_line':fields.one2many('product.inventory.serialize','prod_inv_id','Serial No.'),
              'name':fields.related('product_id','name',relation='product.product',type='char',size=64,invisible=True,store=True),
              }
    
    
    def on_change_product_id(self, cr, uid, ids, location_id, product, uom=False, to_date=False):
        """ Changes UoM and name if product_id changes.
        @param location_id: Location id
        @param product: Changed product_id
        @param uom: UoM product
        @return:  Dictionary of changed values
        """
        warning = {}
        if not product:
            return {'value': {'product_qty': 0.0, 'product_uom': False}}
        obj_product = self.pool.get('product.product').browse(cr, uid, product)
        uom = uom or obj_product.uom_id.id
        if obj_product.serialized:
            warning = {
                    'title': _('Serialize Information !'),
                    'message': _('You have selected a serialize product, Make sure to select serial number. !')
                    }
        amount = self.pool.get('stock.location')._product_get(cr, uid, location_id, [product], {'uom': uom, 'to_date': to_date})[product]
        result = {'product_qty': amount, 'product_uom': uom}
        return {'value': result, 'warning':warning}
    
stock_inventory_line()

