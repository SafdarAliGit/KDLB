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
            "label": _("Sr# "),
            "fieldname": "sr",
            "fieldtype": "Data",
            "width": 100
        },
		{
            "label": _("Party"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("Total Amount"),
            "fieldname": "grand_total",
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
                `tabSales Invoice`.customer_name,
                SUM(`tabSales Invoice`.grand_total) AS grand_total 
            FROM 
                `tabSales Invoice`
            WHERE 
                 {conditions}
            GROUP BY `tabSales Invoice`.customer_name
            """.format(conditions=get_conditions(filters, "Sales Invoice"))

    si_result = frappe.db.sql(si_query, filters, as_dict=1)
    total_grand_total = 0
    sr = 1
    total_customer_name = len(si_result)
    for row in si_result:
        total_grand_total += row["grand_total"]

        row.update({
            "sr": sr
        })
        sr += 1
    si_result.append({
        "sr": _("Total"),
        "customer_name": f"Total parties :  {total_customer_name}",
        "grand_total": total_grand_total
    })
    data.extend(si_result)
    return data





