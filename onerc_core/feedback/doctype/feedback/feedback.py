# Copyright (c) 2026, Kelvin Njenga and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class Feedback(Document):
	def before_insert(self):
		self.submission_date = now_datetime()
  
		if frappe.session.user and frappe.session.user != "Guest":
			self.submitted_by = frappe.session.user

	def validate(self):
		self._fetch_guest()

	def before_save(self):
		#track review status changes
		if (
			self.status in ("Reviewed", "Resolved", "Closed")
			and not self.reviewed_by
			and frappe.session.user != "Guest"
		):
			self.reviewed_by = frappe.session.user
			self.reviewed_on = now_datetime()

	def _fetch_guest(self):
		#Guests must provide both full_name and email
		if not self.submitted_by:
			if not self.full_name:
				frappe.throw(_("Please provide your full name."))
			if not self.email:
				frappe.throw(_("Please provide your email address."))

