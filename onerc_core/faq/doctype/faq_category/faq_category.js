// Copyright (c) 2026, Kelvin Njenga and contributors
// For license information, please see license.txt

frappe.ui.form.on("FAQ Category", {
	refresh(frm) {
		if (!frm.doc.__islocal) {
			frappe.call({
				method: "frappe.client.get_count",
				args: {
					doctype: "FAQ",
					filters: { category: frm.doc.name, status: "Published" },
				},
				callback(r) {
					if (r.message !== undefined) {
						frm.dashboard.add_indicator(
							__("{0} Published FAQ(s)", [r.message]),
							"blue"
						);
					}
				},
			});
		}
	},
});
