# Copyright (c) 2023, TechVentural and contributors
# For license information, please see license.txt

import frappe
from frappe import _

# import frappe
from frappe.model.document import Document
from kdlb.billing.doctype.utils.get_cargo_rate import get_cargo_rate
from kdlb.billing.doctype.utils.get_cost_center_and_income_account import get_cost_center_and_income_account


class VesselFinalReport(Document):
    pass


# WHEN USING SALES INVOICES

# FOR MULTIPLE AGENTS AND SINGLE AGENT-----------------
@frappe.whitelist()
def submit_agent_invoice(source_name):
    source_name = frappe.get_doc("Vessel Final Report", source_name)
    if len(source_name.vessel_final_report_items) > 0:
        if not source_name.multi_agent_invoice_created:
            for item in source_name.vessel_final_report_items:
                try:

                    si = frappe.new_doc("Sales Invoice")

                    customer_group = item.agent_group
                    item_group = source_name.item_group
                    date = source_name.arrival_date

                    rate_dict = get_cargo_rate(customer_group=customer_group , item_group=item_group, date=date)
                    if rate_dict is None:
                        frappe.throw(_("Rate not found"))

                    cost_center_and_income_ac_dict = get_cost_center_and_income_account(source_name.company)

                    si.customer_group = customer_group
                    si.posting_date = source_name.posting_date
                    si.due_date = source_name.due_date
                    si.customer = item.ships_agent
                    si.bill_no = source_name.bill_no
                    si.tc_no = source_name.tc_no
                    si.vessel_code = source_name.vessel_code
                    si.vessel_name = source_name.vessel_name
                    si.berth = source_name.berth
                    si.arrival_date = source_name.arrival_date
                    si.sail_on_date = source_name.sail_on_date
                    si.nature_of_cargo = source_name.nature_of_cargo
                    si.cargo_name = source_name.cargo_name
                    si.item_group = source_name.item_group
                    si.rate_type = source_name.rate_type
                    si.import_teus = item.import_teus__tons
                    si.export_teus = item.export_teus__tons

                    it = si.append("items", {})
                    it.import_teus = item.import_teus__tons
                    it.export_teus = item.export_teus__tons
                    it.item_code = source_name.nature_of_cargo
                    it.surcharge_rate = source_name.surcharge
                    it.qty = item.import_teus__tons + item.export_teus__tons
                    # it.amount = source_name.amount
                    if source_name.rate_type == 'NR':
                        it.rate = rate_dict["normal_rate"]
                        amount = it.qty * it.rate
                        it.surcharge = amount * (it.surcharge_rate / 100)
                        it.amount_after_surcharge = amount + it.surcharge
                    else:
                        it.rate = rate_dict["special_rate"]
                        amount = it.qty * it.rate
                        it.surcharge = amount * (it.surcharge_rate / 100)
                        it.amount_after_surcharge = amount + it.surcharge

                    it.item_name = source_name.cargo_name
                    it.description = source_name.cargo_name
                    it.uom = source_name.uom
                    it.income_account = cost_center_and_income_ac_dict['income_account']
                    it.cost_center = cost_center_and_income_ac_dict['cost_center']
                    si.submit()
                    # return si
                except Exception as error:
                    frappe.throw(_("Error occured in saving invoice for {0}").format(customer_group))

            source_name.multi_agent_invoice_created = 1
            source_name.save()
        else:
            frappe.throw(_("Invoice already created"))
    else:
        if not source_name.agent_invoice_created:
            try:

                si = frappe.new_doc("Sales Invoice")

                customer_group = source_name.abbr_agent
                item_group = source_name.item_group
                date = source_name.arrival_date

                rate_dict = get_cargo_rate(customer_group=customer_group, item_group=item_group, date=date)
                if rate_dict is None:
                    frappe.throw(_("Rate not found"))

                cost_center_and_income_ac_dict = get_cost_center_and_income_account(source_name.company)

                si.customer_group = customer_group
                si.posting_date = source_name.posting_date
                si.due_date = source_name.due_date
                si.customer = source_name.ships_agent
                si.bill_no = source_name.bill_no
                si.tc_no = source_name.tc_no
                si.vessel_code = source_name.vessel_code
                si.vessel_name = source_name.vessel_name
                si.berth = source_name.berth
                si.arrival_date = source_name.arrival_date
                si.sail_on_date = source_name.sail_on_date
                si.nature_of_cargo = source_name.nature_of_cargo
                si.cargo_name = source_name.cargo_name
                si.item_group = source_name.item_group
                si.rate_type = source_name.rate_type
                si.import_teus = source_name.import_teus
                si.export_teus = source_name.export_teus


                it = si.append("items", {})
                it.import_teus = source_name.import_teus
                it.export_teus = source_name.export_teus
                it.item_code = source_name.nature_of_cargo
                it.surcharge_rate = source_name.surcharge
                it.qty = source_name.import_teus + source_name.export_teus
                # it.amount = source_name.amount
                if source_name.rate_type == 'NR':
                    it.rate = rate_dict["normal_rate"]
                    amount = it.qty * it.rate
                    it.surcharge = amount * (it.surcharge_rate / 100)
                    it.amount_after_surcharge = amount + it.surcharge
                else:
                    it.rate = rate_dict["special_rate"]
                    amount = it.qty * it.rate
                    it.surcharge = amount * (it.surcharge_rate / 100)
                    it.amount_after_surcharge = amount + it.surcharge

                it.item_name = source_name.cargo_name
                it.description = source_name.cargo_name
                it.uom = source_name.uom
                it.income_account = cost_center_and_income_ac_dict['income_account']
                it.cost_center = cost_center_and_income_ac_dict['cost_center']
                source_name.agent_invoice_created = 1
                source_name.save()
                si.submit()
                # return si
            except Exception as error:
                frappe.throw(_("Error occured in saving invoice for {0}").format(customer_group))
        else:
            frappe.throw(_("Invoice already created"))



# ------------------FOR STEVEDORE--------------------
@frappe.whitelist()
def submit_stevedore_invoice(source_name):
    source_name = frappe.get_doc("Vessel Final Report", source_name)
    if not source_name.stevedore_invoice_created:
        try:
            si = frappe.new_doc("Sales Invoice")

            customer_group = source_name.abbr_stevedore
            item_group = source_name.item_group
            date = source_name.arrival_date

            rate_dict = get_cargo_rate(customer_group=customer_group, item_group=item_group, date=date)
            if rate_dict is None:
                frappe.throw(_("Rate not found"))

            cost_center_and_income_ac_dict = get_cost_center_and_income_account(source_name.company)
            si.customer_group = customer_group
            si.posting_date = source_name.posting_date
            si.due_date = source_name.due_date
            si.customer = source_name.stevedore
            si.bill_no = source_name.bill_no
            si.tc_no = source_name.tc_no
            si.vessel_code = source_name.vessel_code
            si.vessel_name = source_name.vessel_name
            si.berth = source_name.berth
            si.arrival_date = source_name.arrival_date
            si.sail_on_date = source_name.sail_on_date
            si.nature_of_cargo = source_name.nature_of_cargo
            si.cargo_name = source_name.cargo_name
            si.item_group = source_name.item_group
            si.rate_type = source_name.rate_type
            si.import_teus = source_name.import_teus
            si.export_teus = source_name.export_teus

            it = si.append("items", {})
            it.import_teus = source_name.import_teus
            it.export_teus = source_name.export_teus
            it.item_code = source_name.nature_of_cargo
            it.surcharge_rate = source_name.surcharge
            it.qty = source_name.import_teus + source_name.export_teus
            # it.amount = source_name.amount
            if source_name.rate_type == 'NR':
                it.rate = rate_dict["normal_rate"]
                amount = it.qty * it.rate
                it.surcharge = amount * (it.surcharge_rate / 100)
                it.amount_after_surcharge = amount + it.surcharge
            else:
                it.rate = rate_dict["special_rate"]
                amount = it.qty * it.rate
                it.surcharge = amount * (it.surcharge_rate / 100)
                it.amount_after_surcharge = amount + it.surcharge

            it.item_name = source_name.cargo_name
            it.description = source_name.cargo_name
            it.uom = source_name.uom
            it.income_account = cost_center_and_income_ac_dict['income_account']
            it.cost_center = cost_center_and_income_ac_dict['cost_center']
            source_name.stevedore_invoice_created = 1
            source_name.save()
            si.submit()
            # return si
        except Exception as error:
            frappe.throw(_("Error occured in saving invoice for {0}").format(customer_group))
    else:
        frappe.throw(_("Invoice already created"))


# ------------------FOR KPT--------------------
@frappe.whitelist()
def submit_kpt_invoice(source_name):

    source_name = frappe.get_doc("Vessel Final Report", source_name)
    if not source_name.kpt_invoice_created:
        try:
            si = frappe.new_doc("Sales Invoice")

            customer_group = source_name.abbr_kpt
            item_group = source_name.item_group
            date = source_name.arrival_date

            rate_dict = get_cargo_rate(customer_group=customer_group, item_group=item_group, date=date)
            if rate_dict is None:
                frappe.throw(_("Rate not found"))

            cost_center_and_income_ac_dict = get_cost_center_and_income_account(source_name.company)
            si.customer_group = customer_group
            si.posting_date = source_name.posting_date
            si.due_date = source_name.due_date
            si.customer = source_name.kpt
            si.bill_no = source_name.bill_no
            si.tc_no = source_name.tc_no
            si.vessel_code = source_name.vessel_code
            si.vessel_name = source_name.vessel_name
            si.arrival_date = source_name.arrival_date
            si.sail_on_date = source_name.sail_on_date
            si.nature_of_cargo = source_name.nature_of_cargo
            si.cargo_name = source_name.cargo_name
            si.item_group = source_name.item_group
            si.rate_type = source_name.rate_type
            si.import_teus = source_name.import_teus
            si.export_teus = source_name.export_teus

            it = si.append("items", {})
            it.import_teus = source_name.import_teus
            it.export_teus = source_name.export_teus
            it.item_code = source_name.nature_of_cargo
            it.surcharge_rate = source_name.surcharge
            it.qty = source_name.import_teus + source_name.export_teus
            # it.amount = source_name.amount
            if source_name.rate_type == 'NR':

                it.rate = rate_dict["normal_rate"]
                amount = it.qty * it.rate
                it.surcharge = amount * (it.surcharge_rate / 100)
                it.amount_after_surcharge = amount + it.surcharge
            else:
                it.rate = rate_dict["special_rate"]
                amount = it.qty * it.rate
                it.surcharge = amount * (it.surcharge_rate / 100)
                it.amount_after_surcharge = amount + it.surcharge

            it.item_name = source_name.cargo_name
            it.description = source_name.cargo_name
            it.uom = source_name.uom
            it.income_account = cost_center_and_income_ac_dict['income_account']
            it.cost_center = cost_center_and_income_ac_dict['cost_center']
            source_name.kpt_invoice_created = 1
            source_name.save()
            si.submit()
            # return si
        except:
            frappe.throw(_("Error occured in saving invoice for {0}").format(customer_group))
    else:
        frappe.throw(_("Invoice already created"))
# WHEN USING SALES INVOICES END





