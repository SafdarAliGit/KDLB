# Copyright (c) 2023, TechVentural and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document
from frappe.query_builder.functions import IfNull



class KPTBill(Document):
	pass
@frappe.whitelist()
def save_kpt_bill(**args):
    try:
        # GETTING RATE FROMRATE LIST
        # argumetns========
        kpt_group = args.get('abbr_kpt')
        item_group = args.get('item_group')
        date = args.get('date')
        source_name = args.get('source_name')
        # parent record========
        parent = frappe.qb.DocType("Cargo Rates")
        query = (
            frappe.qb.from_(parent)
            .select(parent.name)
            .where(
                ((parent.customer_group == kpt_group) & (parent.active == 1))
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
    kpt_bill_doc_exists = frappe.db.exists("KPT Bill", {"bill_no": source.name})
    if not kpt_bill_doc_exists:
        try:
            kpt_bill = frappe.new_doc("KPT Bill")

            kpt_bill.year = source.year
            kpt_bill.tc_no = source.tc_no
            kpt_bill.ships_agent = source.ships_agent
            kpt_bill.stevedore = source.stevedore
            kpt_bill.kpt = source.kpt
            kpt_bill.vesel_code = source.vesel_code
            kpt_bill.berth = source.berth
            kpt_bill.arrival_date = source.arrival_date
            kpt_bill.sail_on_date = source.sail_on_date
            kpt_bill.nature_of_cargo = source.nature_of_cargo
            kpt_bill.bill_no = source.bill_no
            kpt_bill.surcharge = source.surcharge
            kpt_bill.ships_agent_name = source.ships_agent_name
            kpt_bill.stevedore_name = source.stevedore_name
            kpt_bill.kpt_name = source.kpt_name
            kpt_bill.vessel_name = source.vessel_name
            kpt_bill.due_date = source.due_date
            kpt_bill.import_teus = source.import_teus
            kpt_bill.export_teus = source.export_teus
            amount = (source.import_teus + source.export_teus) * rate_dic['normal_rate']
            kpt_bill.amount = amount
            kpt_bill.amount_after_surcharge = (amount * (float(source.surcharge_rate) / 100)) + amount
            kpt_bill.surcharge_rate = source.surcharge_rate
            kpt_bill.rate = rate_dic['normal_rate']
            kpt_bill.abbr_agent = kpt_group
            kpt_bill.cargo_name = source.cargo_name
            kpt_bill.docstatus = 1
            kpt_bill.insert()
            frappe.db.commit()
            return {"saved": "KPT Bill Saved"}
        except Exception as error:
            return {"error": error}
    else:
        return {"already_saved": "KPT Bill Already Saved"}
