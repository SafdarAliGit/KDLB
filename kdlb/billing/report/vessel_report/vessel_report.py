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
            "label": _("Voucher Type"),
            "fieldname": "invoice_name",
            "fieldtype": "Link",
            "options": "DocType",
            "width": 120
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 90
        },
        {
            "label": _("Grand Total"),
            "fieldname": "grand_total",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Currency"),
            "fieldname": "currency",
            "width": 90
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Item"),
            "fieldname": "item_code",
            "fieldtype": "Item",
            "width": 120
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Int",
            "width": 90
        },
        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 80
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Paid"),
            "fieldname": "paid_amount",
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

    if doctype == "Journal Entry":
        conditions.append("`tabJournal Entry`.is_opening = 0")

    return " AND ".join(conditions)


def get_account_type_from_name(account_name):
    try:
        account_doc = frappe.get_doc("Account", account_name)
        account_type = account_doc.account_type
        return account_type
    except frappe.DoesNotExistError:
        return None


def get_data(filters):
    data = []
    vr_query = """
            SELECT 
                `tabSales Invoice`.name AS invoice_name,
                `tabSales Invoice`.customer,
                `tabSales Invoice`.grand_total,
                `tabSales Invoice`.currency,
                `tabSales Invoice`.posting_date,
                `tabSales Invoice Item`.item_code,
                `tabSales Invoice Item`.qty,
                `tabSales Invoice Item`.rate,
                `tabSales Invoice Item`.amount,
                `tabGL Entry`.credit as paid_amount
            FROM 
                `tabSales Invoice`
            INNER JOIN 
                `tabSales Invoice Item` ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
            LEFT JOIN 
                `tabGL Entry` ON `tabSales Invoice`.name = `tabGL Entry`.against_voucher
            WHERE 
                 {conditions}
            """.format(conditions=get_conditions(filters, "Sales Invoice"))

    vr_result = frappe.db.sql(vr_query, filters, as_dict=1)

    # ====================CALCULATING TOTAL IN BANK RECEIVED END====================

    # ====================CALCULATING TOTAL IN BANK PAID====================
    # bank_payment_header_dict = [{'voucher_type': '<b><u>Bank Payment</b></u>', 'posting_date': '', 'voucher_no': '',
    #                           'party': '', 'debit': '', 'credit': '', 'grand_total': '',
    #                           'items': ''}]
    # bank_payment_total_dict = {'voucher_type': '<b>Sum</b>', 'posting_date': '-------', 'voucher_no': '-------',
    #                         'party': '-------', 'debit': None, 'credit': 0, 'grand_total': 0,
    #                         'items': '--------------'}
    # total = 0
    # for index, cr in enumerate(bank_payment_result):
    #     total += cr.credit
    #     bank_payment_result[index][
    #         'party'] = f"{bank_payment_result[index]['party']}  {' / ' + bank_payment_result[index]['party_type'] if bank_payment_result[index]['party_type'] else ''} {' / ' + bank_payment_result[index]['party'] if bank_payment_result[index]['party'] else ''}"
    #
    # bank_payment_total_dict['credit'] = total
    # bank_payment_result = bank_payment_header_dict + bank_payment_result
    # bank_payment_result.append(bank_payment_total_dict)
    # ====================CALCULATING TOTAL IN BANK PAID END====================
    #
    # ====================TRANSACTION TYPE FILTER====================
    # if filters.get('transaction_types') == "All":
    #     data.extend(sale_result)
    #     data.extend(purchase_result)
    #     data.extend(cash_receipt_result)
    #     data.extend(cash_payment_result)
    #     data.extend(bank_receipt_result)
    #     data.extend(bank_payment_result)
    # if 'Sales' in filters.get('transaction_types'):
    #     data.extend(sale_result)
    # if 'Purchases' in filters.get('transaction_types'):
    #     data.extend(purchase_result)
    # if 'Cash Receipt' in filters.get('transaction_types'):
    #     data.extend(cash_receipt_result)
    # if 'Cash Payment' in filters.get('transaction_types'):
    #     data.extend(cash_payment_result)
    # if 'Bank Receipt' in filters.get('transaction_types'):
    #     data.extend(bank_receipt_result)
    # if 'Bank Payment' in filters.get('transaction_types'):
    #     data.extend(bank_payment_result)
    #     # ====================FILTERS END====================
    data.extend(vr_result)
    return data
