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
            "label": _("Code"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Party Name"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Import"),
            "fieldname": "import_teus",
            "fieldtype": "Data",
            "width": 120
        },{
            "label": _("Export"),
            "fieldname": "export_teus",
            "fieldtype": "Data",
            "width": 120
        },{
            "label": _("Cargo Handled in Tons"),
            "fieldname": "cargo_in_tons",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Bill Amount"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 200
        },
        {
            "label": _("Amount Received"),
            "fieldname": "credit",
            "fieldtype": "Currency",
            "width": 200
        },
        {
            "label": _("Outstanding"),
            "fieldname": "outstanding_amount",
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
                `tabSales Invoice`.customer,
                `tabSales Invoice`.customer_name,
                SUM(`tabSales Invoice`.import_teus) AS import_teus,
                SUM(`tabSales Invoice`.export_teus) AS export_teus,
                SUM(`tabSales Invoice`.grand_total) AS grand_total, 
                SUM(`tabSales Invoice`.paid_amount) AS paid_amount,
                SUM(`tabSales Invoice`.outstanding_amount) AS outstanding_amount ,
                COALESCE(SUM(`tabGL Entry`.credit), 0) AS credit
            FROM 
                `tabSales Invoice`
            LEFT JOIN 
                `tabGL Entry` ON `tabSales Invoice`.name = `tabGL Entry`.against_voucher AND `tabGL Entry`.credit > 0
            WHERE 
                 {conditions} AND `tabSales Invoice`.item_group='Cargo'
            GROUP BY `tabSales Invoice`.customer,`tabSales Invoice`.customer_name
            """.format(conditions=get_conditions(filters, "Sales Invoice"))

    si_result = frappe.db.sql(si_query, filters, as_dict=1)
    for row in si_result:
        row.update({
            'cargo_in_tons': row.import_teus + row.import_teus,
        })
    total_import_teus = 0
    total_export_teus = 0
    total_grand_total = 0
    total_credit = 0
    total_outstanding_amount = 0
    total_customer_name = len(si_result)
    for row in si_result:
        total_grand_total += row["grand_total"]
        total_credit += row["credit"]
        total_outstanding_amount += row["outstanding_amount"]
        total_import_teus += row["import_teus"]
        total_export_teus += row["export_teus"]
    si_result.append({
        "customer": _("Total"),
        "customer_name": f"Total parties :  {total_customer_name}",
        "import_teus": total_import_teus,
        "export_teus": total_export_teus,
        "cargo_in_tons": total_import_teus + total_export_teus,
        "grand_total": total_grand_total,
        "credit": total_credit,
        "outstanding_amount": total_outstanding_amount
    })
    data.extend(si_result)
    return data





