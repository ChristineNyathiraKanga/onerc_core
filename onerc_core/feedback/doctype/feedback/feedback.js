// Copyright (c) 2026, Kelvin Njenga and contributors
// For license information, please see license.txt

frappe.ui.form.on("Feedback", {
	refresh(frm) {
		frm.trigger("render_action_buttons");
	},


	render_action_buttons(frm) {
		if (frm.doc.__islocal) return;

		const transitions = {
			Open: [["Mark Reviewed", "Reviewed"], ["Resolve", "Resolved"]],
			Reviewed: [["Resolve", "Resolved"], ["Close", "Closed"]],
			Resolved: [["Close", "Closed"], ["Reopen", "Open"]],
			Closed: [["Reopen", "Open"]],
		};

		(transitions[frm.doc.status] || []).forEach(([label, next_status]) => {
			frm.add_custom_button(__(label), () => {
				frappe.prompt(
					{
						fieldname: "reviewer_notes",
						fieldtype: "Small Text",
						label: __("Reviewer Notes (optional)"),
					},
					({ reviewer_notes }) => {
						frappe.call({
							method: 'frappe.client.set_value',
							args: {
								doctype: 'Feedback',
								name: frm.doc.name,
								fieldname: 'status',
								value: next_status
							},
							callback() { frm.reload_doc(); }
							});
					},
					__("Update Status"),
					__(label)
				);
			}, __("Actions"));
		});
	},
});

