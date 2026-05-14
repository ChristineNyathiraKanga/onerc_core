# Copyright (c) 2026, Kenya Red Cross Society and contributors
# For license information, please see license.txt

import frappe


@frappe.whitelist(allow_guest=True)
def get_articles() -> list[dict]:
	names = frappe.get_all(
		"Article",
		filters={"status": "Published", "docstatus": 1},
		pluck="name",
		order_by="published_on desc",
	)
	return [frappe.get_doc("Article", n).as_dict() for n in names]


@frappe.whitelist(allow_guest=True)
def get_article(slug: str) -> dict:
	name = frappe.db.get_value("Article", {"slug": slug, "status": "Published", "docstatus": 1})
	if not name:
		frappe.throw("Article not found", frappe.DoesNotExistError)
	return frappe.get_doc("Article", name).as_dict()


@frappe.whitelist(methods=["POST"])
def create_article(**kwargs) -> dict:
	kwargs["doctype"] = "Article"
	kwargs.setdefault("author", frappe.session.user)
	doc = frappe.get_doc(kwargs)
	doc.insert()
	return doc.as_dict()
