# Copyright (c) 2026, Kelvin Njenga and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class FAQ(Document):
	def validate(self):
		if self.status == "Published" and not self.answer:
			frappe.throw(_("Answer is required before publishing an FAQ."))

	def before_save(self):
		if self.status == "Published" and not self.published_on:
			self.published_on = now_datetime()
		elif self.status != "Published":
			self.published_on = None
