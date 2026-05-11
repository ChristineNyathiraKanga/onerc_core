# Copyright (c) 2026, Kelvin Njenga and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class FAQCategory(Document):
	def validate(self):
		self._validate_unique_name()

	def _validate_unique_name(self):
		filters = {
			"category_name": self.category_name,
			"name": ("!=", self.name or ""),
		}
		if self.company:
			filters["company"] = self.company

		if frappe.db.exists("FAQ Category", filters):
			frappe.throw(
				_("A FAQ Category named '{0}' already exists{1}.").format(
					self.category_name,
					_(" for company {0}").format(self.company) if self.company else "",
				)
			)
