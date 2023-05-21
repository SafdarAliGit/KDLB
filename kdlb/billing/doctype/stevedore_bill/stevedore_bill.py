# Copyright (c) 2023, TechVentural and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document
from frappe.query_builder.functions import IfNull


class StevedoreBill(Document):
    pass


@frappe.whitelist()
def save_stevedore_bill(**args):
    try:
        # GETTING RATE FROMRATE LIST
        # argumetns========
        stevedore_group = args.get('abbr_stevedore')
        item_group = args.get('item_group')
        date = args.get('date')
        source_name = args.get('source_name')
        # parent record========
        parent = frappe.qb.DocType("Cargo Rates")
        query = (
            frappe.qb.from_(parent)
            .select(parent.name)
            .where(
                ((parent.customer_group == stevedore_group) & (parent.active == 1))
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
        rate_dic = {"normal_rate": rate_array[0], "special_rate": rate_array[1]}
    except Exception as error:
        frappe.msgprint(msg="Rate not found, please check cargo rates !", title='Error',
                        raise_exception=error)
    # GETTING RATE FROMRATE LIST END
    #     AGENT BILL ENTRY
    source = frappe.get_doc("Vessel Final Report", source_name)
    stevedore_bill_doc_exists = frappe.db.exists("Stevedore Bill", {"bill_no": source.name})
    if not stevedore_bill_doc_exists:
        try:
            stevedore_bill = frappe.new_doc("Stevedore Bill")

            stevedore_bill.year = source.year
            stevedore_bill.tc_no = source.tc_no
            stevedore_bill.ships_agent = source.ships_agent
            stevedore_bill.stevedore = source.stevedore
            stevedore_bill.kpt = source.kpt
            stevedore_bill.vesel_code = source.vesel_code
            stevedore_bill.berth = source.berth
            stevedore_bill.arrival_date = source.arrival_date
            stevedore_bill.sail_on_date = source.sail_on_date
            stevedore_bill.nature_of_cargo = source.nature_of_cargo
            stevedore_bill.bill_no = source.bill_no
            stevedore_bill.surcharge = source.surcharge
            stevedore_bill.ships_agent_name = source.ships_agent_name
            stevedore_bill.stevedore_name = source.stevedore_name
            stevedore_bill.kpt_name = source.kpt_name
            stevedore_bill.vessel_name = source.vessel_name
            stevedore_bill.due_date = source.due_date
            stevedore_bill.import_teus = source.import_teus
            stevedore_bill.export_teus = source.export_teus
            amount = (source.import_teus + source.export_teus) * rate_dic['normal_rate']
            stevedore_bill.amount = amount
            stevedore_bill.amount_after_surcharge = (amount * (float(source.surcharge_rate) / 100)) + amount
            stevedore_bill.surcharge_rate = source.surcharge_rate
            stevedore_bill.rate = rate_dic['normal_rate']
            stevedore_bill.abbr_agent = stevedore_group
            stevedore_bill.cargo_name = source.cargo_name
            stevedore_bill.docstatus = 1
            stevedore_bill.insert()
            frappe.db.commit()
            return {"saved": "Stevedore Bill Saved"}
        except Exception as error:
            return {"error": error}
    else:
        return {"already_saved": "Stevedore Bill Already Saved"}
