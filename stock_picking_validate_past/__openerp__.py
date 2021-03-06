# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2013 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
############################################################################
#    Coded by: Luis Torres (luis_t@vauxoo.com)
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
{
    'name': 'Stock Validate Past',
    "version" : "1.1",
    'author': 'Vauxoo',
    "category" : "Warehouse Management",
    "website" : "http://www.vauxoo.com/",
    'depends': ['stock',],
    'description': """
  This module add the selection field "type_process_date", if its value = planned_date the field date_create takes the value from date_expected.
  It also writes the proper value on that field so it works correctly from the stock_inventory view
    """,
    'update_xml':[
        'stock_view.xml'],
    'active':False,
    'installable':True
}
