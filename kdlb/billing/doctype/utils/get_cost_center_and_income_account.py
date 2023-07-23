import frappe
from frappe import _

def get_cost_center_and_income_account(company):
    income_account, cost_center = frappe.get_cached_value(
        "Company", company, ["default_income_account", "cost_center"]
    )

    if not income_account:
        frappe.throw(
            _("Please set 'Income account' in Company {0}").format(company)
        )
    if not cost_center:
        frappe.throw(_("Please set 'Cost Center' in Company {0}").format(company))
    data = {'income_account':income_account,'cost_center':cost_center}
    return data
<<<<<<< HEAD

=======
>>>>>>> 41266be (invoices creation done)
