import frappe
from frappe import _, DoesNotExistError
from frappe.query_builder.functions import IfNull


def get_cargo_rate(**args):
    try:
        # GETTING RATE FROM RATE LIST
        # argumetns========
        customer_group = args.get('customer_group')
        item_group = args.get('item_group')
        date = args.get('date')
        # parent record========
        parent = frappe.qb.DocType("Cargo Rates")
        query = (
            frappe.qb.from_(parent)
            .select(parent.name)
            .where(
                ((parent.customer_group == customer_group) & (parent.active == 1))
            )
            .orderby(parent.valid_from, order=frappe.qb.desc)
        )
        if args.get('date'):
            query = query.where(
                (IfNull(parent.valid_from, "2000-01-01") <= date)
                & (IfNull(parent.valid_upto, "2500-12-31") >= date)
            )
        parent_name = query.run()[0][0]

        # child record========
        child = frappe.qb.DocType("Cargo Rates Items")
        query = (
            frappe.qb.from_(child)
            .select(
                child.normal_rate,
                child.special_rate,
            )
            .where((child.parent == parent_name) & (child.item_group == item_group))
        )
        rate_array = query.run()[0]

        rate_dict = {"normal_rate": rate_array[0], "special_rate": rate_array[1]}
        if rate_dict["normal_rate"] == 0:
            frappe.throw(_("Normal rate not set"))
        if rate_dict['special_rate'] == 0:
            frappe.throw(_("Special rate not set"))

    except:
        return None
    return rate_dict
