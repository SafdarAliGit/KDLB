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
            "label": _("Invoice No"),
            "fieldname": "invoice_no",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 100
        },
        {
            "label": _("Tonage Certificate"),
            "fieldname": "tonage_certificate",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("Berth"),
            "fieldname": "berth",
            "fieldtype": "Data",
            "width": 50
        },
        {
            "label": _("Vessel"),
            "fieldname": "vessel_name",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Arrival Date"),
            "fieldname": "arrival_date",
            "fieldtype": "Date",
            "width": 80
        },
        {
            "label": _("Departure Date"),
            "fieldname": "departure_date",
            "fieldtype": "Date",
            "width": 80
        },
        {
            "label": _("Nature Of Cargo"),
            "fieldname": "nature_of_cargo",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Import"),
            "fieldname": "import_teus",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Export"),
            "fieldname": "export_teus",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Total"),
            "fieldname": "total_qty",
            "fieldtype": "Data",
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
    if filters.get("vessel_code"):
        conditions.append(f"`tab{doctype}`.vessel_code = %(vessel_code)s")
    if filters.get("customer"):
        conditions.append(f"`tab{doctype}`.customer = %(customer)s")
    if filters.get("item_group"):
        conditions.append(f"`tab{doctype}`.item_group = %(item_group)s")

    conditions.append(f"`tab{doctype}`.docstatus = 1")  # Include only submitted documents

    return " AND ".join(conditions)


def get_data(filters):
    data = []
    si_query = """
            SELECT 
                `tabSales Invoice`.name AS invoice_no,
                `tabSales Invoice`.tc_no as tonage_certificate,
                `tabSales Invoice`.berth,
                `tabSales Invoice`.vessel_name,
                `tabSales Invoice`.arrival_date,
                `tabSales Invoice`.sail_on_date as departure_date,
                `tabSales Invoice`.cargo_name as nature_of_cargo,
                `tabSales Invoice`.import_teus,
                `tabSales Invoice`.export_teus,
                 `tabSales Invoice`.total_qty
            FROM 
                `tabSales Invoice`
            WHERE 
                 {conditions}
            """.format(conditions=get_conditions(filters, "Sales Invoice"))

    si_result = frappe.db.sql(si_query, filters, as_dict=1)
    data.extend(si_result)
    return data





