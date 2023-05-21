import json

import frappe
import frappe.defaults
from erpnext.selling.doctype.customer.customer import Customer
from frappe import _, msgprint, qb
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from frappe.model.mapper import get_mapped_doc
from frappe.model.naming import set_name_by_naming_series, set_name_from_naming_options
from frappe.model.utils.rename_doc import update_linked_doctypes
from frappe.utils import cint, cstr, flt, get_formatted_email, today
from frappe.utils.user import get_users_with_role

from erpnext.accounts.party import (  # noqa
	get_dashboard_info,
	get_timeline_data,
	validate_party_accounts,
)
from erpnext.utilities.transaction_base import TransactionBase


class CustomerOverrides(Customer):
    def autoname(self):
        cust_master_name = frappe.defaults.get_global_default("cust_master_name")
        if cust_master_name == "Customer Name":
            self.name = self.get_customer_name()
        elif cust_master_name == "Naming Series":
            set_name_by_naming_series(self)
        else:
            self.name = set_name_from_naming_options(frappe.get_meta(self.doctype).autoname, self)

    def get_customer_name(self):

        if frappe.db.get_value("Customer", self.party_code) and not frappe.flags.in_import:
            count = frappe.db.sql(
                """select ifnull(MAX(CAST(SUBSTRING_INDEX(name, ' ', -1) AS UNSIGNED)), 0) from tabCustomer
                 where name like %s""",
                "%{0} - %".format(self.party_code),
                as_list=1,
            )[0][0]
            count = cint(count) + 1

            new_customer_name = "{0} - {1}".format(self.party_code, cstr(count))

            msgprint(
                _("Changed customer name to '{}' as '{}' already exists.").format(
                    new_customer_name, self.party_code
                ),
                title=_("Note"),
                indicator="yellow",
            )

            return new_customer_name

        return self.party_code