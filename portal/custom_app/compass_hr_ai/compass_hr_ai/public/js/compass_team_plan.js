frappe.ui.form.on("Compass Team Plan", {
  refresh(frm) {
    frm.add_custom_button("Compute Team Plan", () => {
      frappe.msgprint("TODO: will call compass_hr_ai.compute_team_plan");
    });
  },
});