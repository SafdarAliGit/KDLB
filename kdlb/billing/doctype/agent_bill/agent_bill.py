# Copyright (c) 2023, TechVentural and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document
from frappe.query_builder.functions import IfNull


class AgentBill(Document):
    pass


@frappe.whitelist()
def save_agent_bill(**args):
    try:
        # GETTING RATE FROM RATE LIST
        # argumetns========
        agent_group = args.get('abbr_agent')
        item_group = args.get('item_group')
        date = args.get('date')
        source_name = args.get('source_name')
        # parent record========
        parent = frappe.qb.DocType("Cargo Rates")
        query = (
            frappe.qb.from_(parent)
            .select(parent.name)
            .where(
                ((parent.customer_group == agent_group) & (parent.active == 1))
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
    agent_bill_doc_exists = frappe.db.exists("Agent Bill", {"bill_no": source.name})
    if not agent_bill_doc_exists:
        try:
            agent_bill = frappe.new_doc("Agent Bill")

            agent_bill.year = source.year
            agent_bill.tc_no = source.tc_no
            agent_bill.ships_agent = source.ships_agent
            agent_bill.stevedore = source.stevedore
            agent_bill.kpt = source.kpt
            agent_bill.vesel_code = source.vesel_code
            agent_bill.berth = source.berth
            agent_bill.arrival_date = source.arrival_date
            agent_bill.sail_on_date = source.sail_on_date
            agent_bill.nature_of_cargo = source.nature_of_cargo
            agent_bill.bill_no = source.bill_no
            agent_bill.surcharge = source.surcharge
            agent_bill.ships_agent_name = source.ships_agent_name
            agent_bill.stevedore_name = source.stevedore_name
            agent_bill.kpt_name = source.kpt_name
            agent_bill.vessel_name = source.vessel_name
            agent_bill.due_date = source.due_date
            agent_bill.import_teus = source.import_teus
            agent_bill.export_teus = source.export_teus
            amount = (source.import_teus + source.export_teus) * rate_dic['normal_rate']
            agent_bill.amount = amount
            agent_bill.amount_after_surcharge = (amount * (float(source.surcharge_rate) / 100)) + amount
            agent_bill.surcharge_rate = source.surcharge_rate
            agent_bill.rate = rate_dic['normal_rate']
            agent_bill.abbr_agent = agent_group
            agent_bill.cargo_name = source.cargo_name
            agent_bill.docstatus = 1
            agent_bill.insert()
            frappe.db.commit()
            return {"saved": "Agent Bill Saved"}
        except Exception as error:
            return {"error": error}
    else:
        return {"already_saved": "Agent Bill Already Saved"}
