
import frappe
from erpnext.setup.doctype.sales_partner.sales_partner import SalesPartner
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.utils import cstr, filter_strip_join
from frappe.website.website_generator import WebsiteGenerator


class SalesPartnerOverrides(SalesPartner):
	def autoname(self):
		self.name = self.agent_code