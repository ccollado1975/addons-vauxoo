# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
############################################################################
#    Coded by: julio (julio@vauxoo.com)
############################################################################
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
from osv import osv,fields
from tools.translate import _

class mrp_production(osv.osv):
    _inherit='mrp.production'
    
    def action_compute(self, cr, uid, ids, properties=[], context=None):
        mrp_pt = self.pool.get('mrp.pt.planified')
        bom_obj = self.pool.get('mrp.bom')
        res = super(mrp_production, self).action_compute(cr,uid,ids,properties=properties,context=context)
        bom_obj = self.pool.get('mrp.bom')
        uom_obj = self.pool.get('product.uom')
        for production in self.browse(cr, uid, ids):
            bom_id = production.bom_id
            if not bom_id:
                continue
            factor = uom_obj._compute_qty(cr, uid, production.product_uom.id, production.product_qty, bom_id.product_uom.id)
            result_subproducts =[]
            res = bom_obj._bom_explode(cr, uid, bom_id, factor / bom_id.product_qty, properties=False, routing_id=False, result_subproducts=result_subproducts)
            for sub_product in result_subproducts:
                data = {
                    'product_id': sub_product['product_id'],
                    'quantity': sub_product['product_qty'],
                    'product_uom': sub_product['product_uom'],
                    'production_id': production.id
                }
                mrp_pt.create(cr,uid,data)
        return res
mrp_production()

