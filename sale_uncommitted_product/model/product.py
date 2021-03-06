#!/usr/bin/python
# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Humberto Arocha <hbto@vauxoo.com>           
#    Planified by: Rafael Silva <rsilvam@vauxoo.com>
#    Audited by: Nhomar Hernandez <nhomar@vauxoo.com>
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################


from osv import fields, osv
from tools.translate import _
import decimal_precision as dp

class product_product(osv.osv):
    _inherit = "product.product"
    
    def _get_product_committed_amount(self, cr, uid, ids, context=None):
        amount = 0.0
        sol_obj = self.pool.get('sale.order.line')
        uom_obj = self.pool.get('product.uom')
        for sol_brw in sol_obj.browse(cr, 1, ids, context=context):
            from_uom_id = sol_brw.product_uom
            to_uom_id = sol_brw.product_id.uom_id
            qty = sol_brw.product_uom_qty
            amount += uom_obj._compute_qty_obj(cr, 1, from_uom_id, qty, to_uom_id, context=context)
        return amount
        
    def _product_committed(self, cr, uid, ids, field_names=None, arg=False, context=None):
        """ Finds the committed products where are on
        committed sale orders.
        @return: Dictionary of values
        """
        
        ru_obj  = self.pool.get('res.users')
        sol_obj = self.pool.get('sale.order.line')
        
        if not field_names:
            field_names = []
        if context is None: context = {}

        ru_brw = ru_obj.browse(cr, 1, uid, context=context)
        context.update({'company_id':ru_brw.company_id and ru_brw.company_id.id})
        
        ARGS = [('order_id','!=',False),('order_id.state','=','committed')]
        
        if context.get('shop', False):
            ARGS+=[('order_id.shop_id','=',context.get('shop', False))]
            
        if context.get('company_id', False):
            ARGS+=[('company_id','=',context.get('company_id', False))]

        res = {}
        
        for id in ids:
            res[id] = {}.fromkeys(field_names, 0.0)
            
        for id in ids:
            #~ TODO: Cambiar por una sentencia sql para no tener que pasar el usuario 1
            sol_ids = sol_obj.search(cr, 1, ARGS+[('product_id','=',id)], context=context)
            amount = 0.0
            if sol_ids and field_names:
                amount = self._get_product_committed_amount(cr, 1, sol_ids, context=context)
            
            for f in field_names:
                if f == 'qty_committed':
                    res[id][f] = amount
                elif f == 'qty_uncommitted':
                    prd_brw = self.browse(cr, uid, id, context = context)
                    res[id][f] = prd_brw.qty_available + prd_brw.outgoing_qty - amount
        return res

    _columns = {
        'qty_committed': fields.function(_product_committed, method=True, type='float', string='Sale Committed', multi='committed', help="Current quantities of committed products in Committe Sale Orders.", digits_compute=dp.get_precision('Product UoM')),
        'qty_uncommitted': fields.function(_product_committed, method=True, type='float', string='Uncommitted', multi='committed', help="Current quantities of committed products in Committe Sale Orders.", digits_compute=dp.get_precision('Product UoM')),
        'warehouse_id': fields.dummy(string='Warehouse', relation='stock.warehouse', type='many2one'),
        'shop_id': fields.dummy(string='Shop', relation='sale.shop', type='many2one'),
    }

product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
