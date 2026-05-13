import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_faq_categories():
	"""Return all available FAQ categories, ordered by sort_order."""
	return frappe.get_all(
		"FAQ Category",
		filters={"is_available": 1},
		fields=["name", "category_name", "description", "sort_order"],
		order_by="sort_order asc, category_name asc",
	)


@frappe.whitelist(allow_guest=True)
def get_faq_list(category=None, search=None):
	"""Return published FAQs, optionally filtered by category or search term"""
	filters = {"status": "Published"}
	if category:
		filters["category"] = category

	or_filters = None
	if search:
		or_filters = [
			["question", "like", f"%{search}%"],
			["answer", "like", f"%{search}%"],
		]

	return frappe.get_all(
		"FAQ",
		filters=filters,
		or_filters=or_filters,
		fields=[
			"name", "question", "answer", "category",
			"sort_order", "helpful", "not_helpful", "published_on",
		],
		order_by="sort_order asc, published_on desc",
	)


@frappe.whitelist(allow_guest=True)
def get_faq(name):
	"""Return a single published FAQ by document name"""
	doc = frappe.get_doc("FAQ", name)
	if doc.status != "Published":
		frappe.throw(_("FAQ not found"), frappe.DoesNotExistError)
	return doc.as_dict()


@frappe.whitelist(allow_guest=True)
def vote_faq(name, vote):
	"""Atomically increment the helpful or not_helpful counter on a published FAQ"""
	if vote not in ("helpful", "not_helpful"):
		frappe.throw(_("Invalid vote. Must be 'helpful' or 'not_helpful'."))

	status = frappe.db.get_value("FAQ", name, "status")
	if not status:
		frappe.throw(_("FAQ not found"), frappe.DoesNotExistError)
	if status != "Published":
		frappe.throw(_("Cannot vote on an unpublished FAQ."))

	frappe.db.sql(
		f"UPDATE `tabFAQ` SET `{vote}` = COALESCE(`{vote}`, 0) + 1 WHERE `name` = %s",
		(name,),
	)
	frappe.db.commit()

	new_count = frappe.db.get_value("FAQ", name, vote)
	return {"name": name, "vote": vote, "count": new_count}
