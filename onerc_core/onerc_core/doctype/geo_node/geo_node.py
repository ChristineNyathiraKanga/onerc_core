# Copyright (c) 2026, Kelvin Njenga and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class GeoNode(NestedSet):
	def autoname(self):
		self.name = f"{self.geo_level}-{self.geo_node_name}"
