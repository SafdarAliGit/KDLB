# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _


def execute(filters=None):
    if not filters:
        filters = {}
    data = []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def decimal_format(value, decimals):
    formatted_value = "{:.{}f}".format(value, decimals)
    return formatted_value


def get_columns():
    columns = [
        {
            "label": _("Party Type"),
            "fieldname": "customer_group",
            "fieldtype": "Data",
            "options": "Customer Group",
            "width": 200
        },
        {
            "label": _("Party"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("No Of Bills"),
            "fieldname": "no_of_bills",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("Bill Amount"),
            "fieldname": "bill_amount",
            "fieldtype": "Currency",
            "width": 200
        }

    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("from_date"):
        conditions.append(f"`tab{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`tab{doctype}`.posting_date <= %(to_date)s")
    if filters.get("vessel_code"):
        conditions.append(f"`tab{doctype}`.vessel_code = %(vessel_code)s")
    if filters.get("customer_group"):
        conditions.append(f"`tab{doctype}`.customer_group = %(customer_group)s")

    conditions.append(f"`tab{doctype}`.docstatus = 1")  # Include only submitted documents

    return " AND ".join(conditions)


def get_data(filters):
    data = []
    si_query = """
            SELECT 
                `tabSales Invoice`.customer_group,
                `tabSales Invoice`.customer_name,
                COUNT(`tabSales Invoice`.name) AS no_of_bills,
                SUM(`tabSales Invoice`.grand_total) AS bill_amount 
            FROM 
                `tabSales Invoice`
            WHERE 
                 {conditions}
            GROUP BY `tabSales Invoice`.customer_group, `tabSales Invoice`.customer
            """.format(conditions=get_conditions(filters, "Sales Invoice"))

    si_result = frappe.db.sql(si_query, filters, as_dict=1)
    total_no_of_bills = 0
    total_bill_amount = 0
    total_customer_name = len(si_result)
    for row in si_result:
        total_no_of_bills += row["no_of_bills"]
        total_bill_amount += row["bill_amount"]
    si_result.append({
        "customer_group": _("Total"),
        "customer_name": f"Total parties :  {total_customer_name}",
        "no_of_bills": total_no_of_bills,
        "bill_amount": total_bill_amount
    })
    data.extend(si_result)
    return data





