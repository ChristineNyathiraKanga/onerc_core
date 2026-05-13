// Copyright (c) 2026, Kelvin Njenga and contributors
// For license information, please see license.txt

frappe.ui.form.on("FAQ", {
	refresh(frm) {
        //action status change
		if (!frm.doc.__islocal) {
			if (frm.doc.status === "Draft") {
				frm.add_custom_button(__("Publish"), () => {
					frm.set_value("status", "Published");
					frm.save();
				}, __("Actions"));
			}

			if (frm.doc.status === "Published") {
				frm.add_custom_button(__("Archive"), () => {
					frm.set_value("status", "Archived");
					frm.save();
				}, __("Actions"));
			}

			if (frm.doc.status === "Archived") {
				frm.add_custom_button(__("Restore to Draft"), () => {
					frm.set_value("status", "Draft");
					frm.save();
				}, __("Actions"));
			}
		}
	},
});
