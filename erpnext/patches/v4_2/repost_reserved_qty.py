# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from erpnext.utilities.repost_stock import update_bin_qty, get_reserved_qty

def execute():
	repost_for = frappe.db.sql("""
		select 
			distinct item_code, warehouse 
		from 
			(
				(
					select distinct item_code, warehouse 
								from `tabSales Order Item` where docstatus=1
				) UNION (
					select distinct item_code, warehouse 
					from `tabPacked Item` where docstatus=1 and parenttype='Sales Order'
				)
			) items
	""")
	
	for item_code, warehouse in repost_for:
			update_bin_qty(item_code, warehouse, {
				"reserved_qty": get_reserved_qty(item_code, warehouse)
			})