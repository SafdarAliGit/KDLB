# Copyright (c) 2023, TechVentural and contributors
# For license information, please see license.txt
import frappe
from erpnext.accounts.utils import get_fiscal_years
# import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries, make_autoname
from frappe.utils import today


class Saptl(Document):

	def on_submit(self):
		# prefix = 'ACC-GLE-.YYYY.-.#####'
		# name = make_autoname(prefix)
		debit = {
			'company': "Shiping Company",
			'posting_date': today(),
			'transaction_date': today(),
			'voucher_type': 'Saptl',
			'voucher_no': self.name,
			'aging_date': today(),
			'remarks': 'remarks',
			'fiscal_year': '2022-2023',
			'debit': self.total_amount,
			'credit': 0,
			'debit_in_account_currency':self.total_amount,
			'credit_in_account_currency':0,
			'cost_center': '',
			'is_opening':"No",
			"account": 'Debtors - SC',
			"against": 'Sales - SC',
			"party":self.customer,
			"party_type":'Customer',
			"against_voucher":self.name,
			"against_voucher_type":'Saptl',
			"against_voucher_no":self.name,
			"due_date":self.due_date
		}
		gl = frappe.new_doc('GL Entry')
		gl.company = debit.get('company')
		# gl.name = name
		gl.posting_date = debit.get('posting_date')
		gl.transaction_date = debit.get('transaction_date')
		gl.voucher_type = debit.get('voucher_type')
		gl.voucher_no = debit.get('voucher_no')
		gl.aging_date = debit.get('aging_date')
		gl.remarks = debit.get('remarks')
		gl.fiscal_year = debit.get('fiscal_year')
		gl.debit = debit.get('debit')
		gl.credit = debit.get('credit')
		gl.debit_in_account_currency=debit.get('debit_in_account_currency')
		gl.credit_in_account_currency=debit.get('credit_in_account_currency')
		gl.cost_center = debit.get('cost_center')
		gl.is_opening = debit.get('is_opening')
		gl.account = debit.get('account')
		gl.against = debit.get('against')
		gl.party = debit.get('party')
		gl.party_type = debit.get('party_type')
		gl.against_voucher = debit.get('against_voucher')
		gl.against_voucher_type = debit.get('against_voucher_type')
		gl.against_voucher_no = debit.get('against_voucher_no')
		gl.due_date = debit.get('due_date')
		gl.save()
		frappe.db.commit()

		credit = {
			'company': "Shiping Company",
			'posting_date': today(),
			'transaction_date': today(),
			'voucher_type': 'Saptl',
			'voucher_no': self.name,
			'aging_date': today(),
			'remarks': 'remarks',
			'fiscal_year': '2022-2023',
			'debit': 0,
			'credit':self.total_amount,
			'debit_in_account_currency':0,
			'credit_in_account_currency':self.total_amount,
			'cost_center': 'Main - SC',
			'is_opening': "No",
			"account": 'Sales - SC',
			"against": self.customer,
			"party": '',
			"party_type": '',
			"against_voucher": '',
			"against_voucher_type": '',
			"against_voucher_no": self.name,
			"due_date": ''
		}
		gl = frappe.new_doc('GL Entry')
		gl.company = credit.get('company')
		# gl.name = name
		gl.posting_date = credit.get('posting_date')
		gl.transaction_date = credit.get('transaction_date')
		gl.voucher_type = credit.get('voucher_type')
		gl.voucher_no = credit.get('voucher_no')
		gl.aging_date = credit.get('aging_date')
		gl.remarks = credit.get('remarks')
		gl.fiscal_year = credit.get('fiscal_year')
		gl.debit = credit.get('debit')
		gl.credit = credit.get('credit')
		gl.debit_in_account_currency = credit.get('debit_in_account_currency')
		gl.credit_in_account_currency = credit.get('credit_in_account_currency')
		gl.cost_center = credit.get('cost_center')
		gl.is_opening = credit.get('is_opening')
		gl.account = credit.get('account')
		gl.against = credit.get('against')
		gl.party = credit.get('party')
		gl.party_type = credit.get('party_type')
		gl.against_voucher = credit.get('against_voucher')
		gl.against_voucher_type = credit.get('against_voucher_type')
		gl.against_voucher_no = credit.get('against_voucher_no')
		gl.due_date = credit.get('due_date')
		gl.save()
		frappe.db.commit()


@frappe.whitelist()
def fetch_saptl_rate(**args):
	# date = datetime.strptime(args.get('date'), '%Y-%m-%d')
	cargo_code = args.get('cargo_code')
	date = args.get('date')
	sr = frappe.qb.DocType("Cargo Rates")
	query = (
		frappe.qb.from_(sr)
		.select(sr.rate)
		.where(
			(sr.cargo_code == cargo_code)
		)
	)

	rate = query.run()[0][0]
	return {"rate":rate}

@frappe.whitelist()
def get_items():
	saptl_rates = frappe.get_list("Saptl Rates", fields=["cargo_code","rate"])
	return saptl_rates