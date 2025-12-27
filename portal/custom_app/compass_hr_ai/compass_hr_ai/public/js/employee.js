frappe.ui.form.on("Employee", {
  refresh(frm) {
    frm.add_custom_button("Generate Career Plan", () => {
      frappe.msgprint("TODO: will call compass_hr_ai.generate_career_plan");
    });

    frm.add_custom_button("Refresh Skills from Resume", () => {
      frappe.msgprint("TODO: will call compass_hr_ai.refresh_skills_from_resume");
    });
  },
});