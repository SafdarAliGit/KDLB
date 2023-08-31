import frappe


@frappe.whitelist()
def update_invoice_fields():
    # Fetch Sales Invoices with docstatus <= 1
    try:
        sales_invoices = frappe.get_all("Sales Invoice",
                                        filters={"docstatus": ["<=", 1]},
                                        fields=["name"])

        for invoice in sales_invoices:
            invoice_doc = frappe.get_doc("Sales Invoice", invoice.name)
            invoice_item = frappe.get_all("Sales Invoice Item",
                                          filters={"parent": invoice.name},
                                          fields=["surcharge_rate", "surcharge", "amount_after_surcharge"],
                                          limit=1)  # Limit to one item

            if invoice_item:
                # Update the fields in Sales Invoice
                invoice_doc.surcharge_rate = invoice_item[0].surcharge_rate
                invoice_doc.surcharge = invoice_item[0].surcharge
                invoice_doc.amount_after_surcharge = invoice_item[0].amount_after_surcharge
                invoice_doc.save()
        return "success"
    except:
        return None
