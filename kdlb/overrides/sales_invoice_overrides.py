import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from erpnext.setup.doctype.sales_partner.sales_partner import SalesPartner
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.model.naming import getseries, make_autoname
from frappe.utils import cstr, filter_strip_join
from frappe.website.website_generator import WebsiteGenerator


class SalesInvoiceOverrides(SalesInvoice):
    def autoname(self):
        if self.customer_group == "AGENT":
<<<<<<< HEAD
            prefix = 'A-.YYYY.-'
        elif self.customer_group == "STEVEDORE":
            prefix = 'S-.YYYY.-'
        elif self.customer_group == "KPT":
            prefix = 'K-.YYYY.-'
=======
            prefix = 'A-.DD.-.MM.-.YYYY.-'
        elif self.customer_group == "STEVEDORE":
            prefix = 'S-.DD.-.MM.-.YYYY.-'
        elif self.customer_group == "KPT":
            prefix = 'K-.DD.-.MM.-.YYYY.-'
>>>>>>> 41266be (invoices creation done)
        else:
            frappe.msgprint(msg="Wrong naming !", title='Error')
        self.name = make_autoname(prefix+'.########')
