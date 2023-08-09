# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def decimal_format(value, decimals):
    formatted_value = "{:.{}f}".format(value, decimals)
    return formatted_value


def get_columns():
    columns = [
        {
            "label": _("Bill Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Vessel Name"),
            "fieldname": "vessel_name",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Arrival Date"),
            "fieldname": "arrival_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Total Amount"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Paid Amount"),
            "fieldname": "paid_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Outstanding Amount"),
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "width": 120
        }
    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("from_date"):
        conditions.append(f"`tab{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`tab{doctype}`.posting_date <= %(to_date)s")

    conditions.append(f"`tab{doctype}`.docstatus = 1")  # Include only submitted documents

    return " AND ".join(conditions)


def get_data(filters):
    data = []
    si_query = """
            SELECT 
                `tabSales Invoice`.name AS invoice_name,
                `tabSales Invoice`.vessel_name,
                `tabSales Invoice`.posting_date,
                `tabSales Invoice`.vessel_name,
                `tabSales Invoice`.arrival_date,
                `tabSales Invoice`.grand_total as grand_total,
                `tabSales Invoice`.outstanding_amount as outstanding_amount,
                 grand_total - outstanding_amount as paid_amount
            FROM 
                `tabSales Invoice`
            INNER JOIN 
                `tabSales Invoice Item` ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
            LEFT JOIN 
                `tabGL Entry` ON `tabSales Invoice`.name = `tabGL Entry`.against_voucher
            WHERE 
                 {conditions}
            """.format(conditions=get_conditions(filters, "Sales Invoice"))

    si_result = frappe.db.sql(si_query, filters, as_dict=1)
    data.extend(si_result)
    return data
