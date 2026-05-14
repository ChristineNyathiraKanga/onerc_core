# Copyright (c) 2026, Kenya Red Cross Society and contributors
# For license information, please see license.txt

import re

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, now, now_datetime


WORDS_PER_MINUTE = 200


class Article(Document):
	def validate(self):
		self.set_slug()
		self.set_read_time()
		self.validate_scheduled_publish_at()
		self.set_published_on()
		self.set_meta_defaults()

	def set_slug(self):
		if self.slug:
			return
		base = slugify(self.title)
		slug = base
		i = 2
		while frappe.db.exists(
			"Article", {"slug": slug, "name": ["!=", self.name or ""]}
		):
			slug = f"{base}-{i}"
			i += 1
		self.slug = slug

	def set_read_time(self):
		text = re.sub(r"<[^>]+>", " ", self.body or "")
		words = len(text.split())
		self.read_time = max(1, round(words / WORDS_PER_MINUTE)) if words else 0

	def validate_scheduled_publish_at(self):
		if self.status != "Scheduled":
			return
		if not self.scheduled_publish_at:
			frappe.throw(frappe._("Scheduled Publish At is required when status is Scheduled."))
		if get_datetime(self.scheduled_publish_at) <= now_datetime():
			frappe.throw(frappe._("Scheduled Publish At must be in the future."))

	def set_published_on(self):
		if self.status == "Published" and not self.published_on:
			self.published_on = now()


	def set_meta_defaults(self):
		if not self.meta_title:
			self.meta_title = self.title
		if not self.meta_description:
			self.meta_description = self.summary


def slugify(value: str) -> str:
	value = (value or "").lower()
	value = re.sub(r"[^a-z0-9]+", "-", value)
	return value.strip("-")


@frappe.whitelist(allow_guest=True)
def increment_view_count(name: str) -> int:
	if not frappe.db.exists("Article", name):
		frappe.throw(frappe._("Article {0} not found").format(name), frappe.DoesNotExistError)
	new_count = (frappe.db.get_value("Article", name, "view_count") or 0) + 1
	frappe.db.set_value("Article", name, "view_count", new_count, update_modified=False)
	return new_count


def publish_scheduled_articles():
	"""Publish submitted (approved) articles whose scheduled time has arrived.

	Runs from scheduler_events in hooks.py. Only acts on submitted (docstatus=1)
	articles in the Scheduled status — drafts and cancelled rows are ignored,
	which is what makes this gated on approval.
	"""
	due = frappe.get_all(
		"Article",
		filters={
			"status": "Scheduled",
			"docstatus": 1,
			"scheduled_publish_at": ["<=", now_datetime()],
		},
		pluck="name",
	)
	for name in due:
		try:
			frappe.db.set_value(
				"Article",
				name,
				{"status": "Published", "published_on": now()},
				update_modified=False,
			)
		except Exception:
			frappe.log_error(frappe.get_traceback(), f"publish_scheduled_articles failed for {name}")
	if due:
		frappe.db.commit()
