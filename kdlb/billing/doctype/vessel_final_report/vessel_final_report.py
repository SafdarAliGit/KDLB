# Copyright (c) 2023, TechVentural and contributors
# For license information, please see license.txt

import frappe
# import frappe
from frappe.model.document import Document
from kdlb.billing.doctype.utils.get_cargo_rate import get_cargo_rate
from kdlb.billing.doctype.utils.get_cost_center_and_income_account import get_cost_center_and_income_account


class VesselFinalReport(Document):
    pass


# WHEN USING SALES INVOICES
# ------------------FOR AGENT-----------------
@frappe.whitelist()
def submit_agent_invoice(source_name):
    try:
        source_name = frappe.get_doc("Vessel Final Report", source_name)
        si = frappe.new_doc("Sales Invoice")

        customer_group = source_name.abbr_agent
        item_group = source_name.item_group
        date = source_name.arrival_date
        rate_dict = get_cargo_rate(customer_group=customer_group, item_group=item_group, date=date)
        cost_center_and_income_ac_dict = get_cost_center_and_income_account(source_name.company)
        si.customer_group = customer_group
        si.posting_date = source_name.posting_date
        si.due_date = source_name.due_date
        si.customer = source_name.ships_agent
        si.bill_no = source_name.bill_no
        si.tc_no = source_name.tc_no
        si.vessel_code = source_name.vessel_code
        si.vessel_name = source_name.vessel_name
        si.arrival_date = source_name.arrival_date
        si.sail_on_date = source_name.sail_on_date
        si.nature_of_cargo = source_name.nature_of_cargo
        si.item_group = source_name.item_group
        si.import_teus = source_name.import_teus
        si.export_teus = source_name.export_teus

        it = si.append("items", {})
        it.item_code = source_name.nature_of_cargo
        it.qty = source_name.import_teus + source_name.export_teus
        # it.amount = source_name.amount
        it.rate = rate_dict["normal_rate"]
        it.item_name = source_name.cargo_name
        it.description = source_name.cargo_name
        it.uom = source_name.uom
        it.income_account = cost_center_and_income_ac_dict['income_account']
        it.cost_center = cost_center_and_income_ac_dict['cost_center']
        si.submit()
        # return si
    except Exception as error:
        frappe.msgprint(msg="Some error occured !", title='Error',
                        raise_exception=error)
# ------------------FOR STEVEDORE--------------------
@frappe.whitelist()
def submit_stevedore_invoice(source_name):
    try:
        source_name = frappe.get_doc("Vessel Final Report", source_name)
        si = frappe.new_doc("Sales Invoice")

        customer_group = source_name.abbr_stevedore
        item_group = source_name.item_group
        date = source_name.arrival_date
        rate_dict = get_cargo_rate(customer_group=customer_group, item_group=item_group, date=date)
        cost_center_and_income_ac_dict = get_cost_center_and_income_account(source_name.company)
        si.customer_group = customer_group
        si.posting_date = source_name.posting_date
        si.due_date = source_name.due_date
        si.customer = source_name.stevedore
        si.bill_no = source_name.bill_no
        si.tc_no = source_name.tc_no
        si.vessel_code = source_name.vessel_code
        si.vessel_name = source_name.vessel_name
        si.arrival_date = source_name.arrival_date
        si.sail_on_date = source_name.sail_on_date
        si.nature_of_cargo = source_name.nature_of_cargo
        si.item_group = source_name.item_group
        si.import_teus = source_name.import_teus
        si.export_teus = source_name.export_teus

        it = si.append("items", {})
        it.item_code = source_name.nature_of_cargo
        it.qty = source_name.import_teus + source_name.export_teus
        # it.amount = source_name.amount
        it.rate = rate_dict["normal_rate"]
        it.item_name = source_name.cargo_name
        it.description = source_name.cargo_name
        it.uom = source_name.uom
        it.income_account = cost_center_and_income_ac_dict['income_account']
        it.cost_center = cost_center_and_income_ac_dict['cost_center']
        si.submit()
        # return si
    except Exception as error:
        frappe.msgprint(msg="Some error occured !", title='Error',
                        raise_exception=error)

# ------------------FOR KPT--------------------
@frappe.whitelist()
def submit_kpt_invoice(source_name):
    try:
        source_name = frappe.get_doc("Vessel Final Report", source_name)
        si = frappe.new_doc("Sales Invoice")

        customer_group = source_name.abbr_kpt
        item_group = source_name.item_group
        date = source_name.arrival_date
        rate_dict = get_cargo_rate(customer_group=customer_group, item_group=item_group, date=date)
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
        si.item_group = source_name.item_group
        si.import_teus = source_name.import_teus
        si.export_teus = source_name.export_teus

        it = si.append("items", {})
        it.item_code = source_name.nature_of_cargo
        it.qty = source_name.import_teus + source_name.export_teus
        # it.amount = source_name.amount
        it.rate = rate_dict["normal_rate"]
        it.item_name = source_name.cargo_name
        it.description = source_name.cargo_name
        it.uom = source_name.uom
        it.income_account = cost_center_and_income_ac_dict['income_account']
        it.cost_center = cost_center_and_income_ac_dict['cost_center']
        si.submit()
        # return si
    except Exception as error:
        frappe.msgprint(msg="Some error occured !", title='Error',
                        raise_exception=error)
# WHEN USING SALES INVOICES END

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields = {
    #         'year': self.year,
    #         'tc_no': self.tc_no,
    #         'ships_agent': None,
    #         'stevedore': None,
    #         'kpt': None,
    #         'vesel_code': self.vesel_code,
    #         'berth': self.berth,
    #         'arrival_date': self.arrival_date,
    #         'sail_on_date': self.sail_on_date,
    #         'nature_of_cargo': self.nature_of_cargo,
    #         'bill_no': self.bill_no,
    #         'surcharge': self.surcharge,
    #         'ships_agent_name': None,
    #         'stevedore_name': None,
    #         'kpt_name': None,
    #         'vessel_name': self.vessel_name,
    #         'due_date': self.due_date,
    #         'import_teus': self.import_teus,
    #         'export_teus': self.export_teus,
    #         'amount': self.amount,
    #         'amount_after_surcharge': self.amount_after_surcharge,
    #         'surcharge_rate': self.surcharge_rate,
    #         'abbr_agent': None,
    #         'abbr_stevedore': None,
    #         'abbr_kpt': None,
    #         'rate': self.rate
    #     }
    #
    # def on_submit(self):
    # def autoname(self):
    #     print(f"-----------------Auton name ran---------------------------")
    #     # if self.fields['abbr_agent']:
    #     #     prefix = f"{self.abbr_agent}-.DD.-.MM.-.YYYY.-"
    #     #     self.name = make_autoname(prefix, 8)
    #     # if self.fields['stevedore']:
    #     #     prefix = f"{self.stevedore}-.DD.-.MM.-.YYYY.-"
    #     #     self.name = make_autoname(prefix, 8)
    #     # if self.fields['kpt']:
    #     #     prefix = f"{self.kpt}-.DD.-.MM.-.YYYY.-"
    #     #     self.name = make_autoname(prefix, 8)
    #
    # def save(self, *args, **kwargs):
    #     # ................................. AGENT BILL SAVING
    #     agent_doc = frappe.new_doc('Bill Entry')
    #
    #     self.fields['ships_agent'] = self.ships_agent
    #     self.fields['abbr_agent'] = self.abbr_agent
    #     self.fields['ships_agent_name'] = self.ships_agent_name
    #     # self.autoname()
    #     print("----------------------i am in agent doc----------------------")
    #     agent_doc.update(self.fields)
    #     agent_doc.insert()
    #     # ................................. STEVEDORE BILL SAVING
    #     stevedore_doc = frappe.new_doc('Bill Entry')
    #
    #     self.fields['stevedore'] = self.stevedore
    #     self.fields['abbr_stevedore'] = self.abbr_stevedore
    #     self.fields['stevedore_name'] = self.stevedore_name
    #
    #     self.fields['ships_agent'] = None
    #     self.fields['abbr_agent'] = None
    #     self.fields['ships_agent_name'] = None
    #     # self.autoname()
    #     print("----------------------i am in stevedore doc----------------------")
    #     stevedore_doc.update(self.fields)
    #     stevedore_doc.insert()
    #     # ................................. KPT BILL SAVING
    #     kpt_doc = frappe.new_doc('Bill Entry')
    #
    #     self.fields['kpt'] = self.kpt
    #     self.fields['abbr_kpt'] = self.abbr_kpt
    #     self.fields['kpt_name'] = self.kpt_name
    #
    #     self.fields['stevedore'] = None
    #     self.fields['abbr_stevedore'] = None
    #     self.fields['stevedore_name'] = None
    #     print("----------------------i am in kpt doc----------------------")
    #     # self.autoname()
    #     kpt_doc.update(self.fields)
    #     kpt_doc.insert()

# .................................

# debit = {
# 	'company': "Shiping Company",
# 	'posting_date': today(),
# 	'transaction_date': today(),
# 	'voucher_type': 'Bill Entry',
# 	'voucher_no': self.name,
# 	'aging_date': today(),
# 	'remarks': 'remarks',
# 	'fiscal_year': '2022-2023',
# 	'debit': self.amount,
# 	'credit': 0,
# 	'debit_in_account_currency': self.amount,
# 	'credit_in_account_currency': 0,
# 	'cost_center': '',
# 	'is_opening': "No",
# 	"account": 'Debtors - SC',
# 	"against": 'Sales - SC',
# 	"party": self.party_code,
# 	"party_type": 'Customer',
# 	"against_voucher": self.name,
# 	"against_voucher_type": 'Bill Entry',
# 	"against_voucher_no": self.name,
# 	"due_date": self.due_date
# }
# gl = frappe.new_doc('GL Entry')
# gl.company = debit.get('company')
# # gl.name = name
# gl.posting_date = debit.get('posting_date')
# gl.transaction_date = debit.get('transaction_date')
# gl.voucher_type = debit.get('voucher_type')
# gl.voucher_no = debit.get('voucher_no')
# gl.aging_date = debit.get('aging_date')
# gl.remarks = debit.get('remarks')
# gl.fiscal_year = debit.get('fiscal_year')
# gl.debit = debit.get('debit')
# gl.credit = debit.get('credit')
# gl.debit_in_account_currency = debit.get('debit_in_account_currency')
# gl.credit_in_account_currency = debit.get('credit_in_account_currency')
# gl.cost_center = debit.get('cost_center')
# gl.is_opening = debit.get('is_opening')
# gl.account = debit.get('account')
# gl.against = debit.get('against')
# gl.party = debit.get('party')
# gl.party_type = debit.get('party_type')
# gl.against_voucher = debit.get('against_voucher')
# gl.against_voucher_type = debit.get('against_voucher_type')
# gl.against_voucher_no = debit.get('against_voucher_no')
# gl.due_date = debit.get('due_date')
# gl.save()
# frappe.db.commit()
#
# credit = {
# 	'company': "Shiping Company",
# 	'posting_date': today(),
# 	'transaction_date': today(),
# 	'voucher_type': 'Bill Entry',
# 	'voucher_no': self.name,
# 	'aging_date': today(),
# 	'remarks': 'remarks',
# 	'fiscal_year': '2022-2023',
# 	'debit': 0,
# 	'credit': self.amount,
# 	'debit_in_account_currency': 0,
# 	'credit_in_account_currency': self.amount,
# 	'cost_center': 'Main - SC',
# 	'is_opening': "No",
# 	"account": 'Sales - SC',
# 	"against": self.party_code,
# 	"party": '',
# 	"party_type": '',
# 	"against_voucher": '',
# 	"against_voucher_type": '',
# 	"against_voucher_no": self.name,
# 	"due_date": ''
# }
# gl = frappe.new_doc('GL Entry')
# gl.company = credit.get('company')
# # gl.name = name
# gl.posting_date = credit.get('posting_date')
# gl.transaction_date = credit.get('transaction_date')
# gl.voucher_type = credit.get('voucher_type')
# gl.voucher_no = credit.get('voucher_no')
# gl.aging_date = credit.get('aging_date')
# gl.remarks = credit.get('remarks')
# gl.fiscal_year = credit.get('fiscal_year')
# gl.debit = credit.get('debit')
# gl.credit = credit.get('credit')
# gl.debit_in_account_currency = credit.get('debit_in_account_currency')
# gl.credit_in_account_currency = credit.get('credit_in_account_currency')
# gl.cost_center = credit.get('cost_center')
# gl.is_opening = credit.get('is_opening')
# gl.account = credit.get('account')
# gl.against = credit.get('against')
# gl.party = credit.get('party')
# gl.party_type = credit.get('party_type')
# gl.against_voucher = credit.get('against_voucher')
# gl.against_voucher_type = credit.get('against_voucher_type')
# gl.against_voucher_no = credit.get('against_voucher_no')
# gl.due_date = credit.get('due_date')
# gl.save()
# frappe.db.commit()

# @frappe.whitelist()
# def fetch_cargo_rate(**args):
#     # date = datetime.strptime(args.get('date'), '%Y-%m-%d')
#     item_group = args.get('cargo_code')
#     date = args.get('date')
#     # rate = frappe.db.get_value('Cargo Rates', {'cargo_code': cargo_code, 'date':date}, ['normal_rate'])
#     # return rate
#
#     cr = frappe.qb.DocType("Cargo Rates")
#     query = (
#         frappe.qb.from_(cr)
#         .select(cr.normal_rate)
#         .where(
#             (cr.cargo_code == cargo_code)
#         )
#         .orderby(cr.valid_from, order=frappe.qb.desc)
#     )
#
#     if args.get('date'):
#         query = query.where(
#             (IfNull(cr.valid_from, "2000-01-01") <= date)
#             & (IfNull(cr.valid_upto, "2500-12-31") >= date)
#         )
#     rate = query.run()[0][0]
#     return {"normal_rate": rate}
