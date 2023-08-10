// Copyright (c) 2023, TechVentural and contributors
// For license information, please see license.txt
/* eslint-disable */



frappe.query_reports["Party Wise Tonage Register"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 1
        },
        {
            "fieldname": "customer_group",
            "label": __("Customer Group"),
            "fieldtype": "Link",
            "options": "Customer Group",
            "get_query": function () {
                return {
                    filters: {"is_group": 0}
                };
            }
        },
        {
            "fieldname": "customer",
            "label": __("Customer Code"),
            "fieldtype": "Link",
            "options": "Customer",
            "get_query": function () {
                var customer_group = frappe.query_report.get_filter_value('customer_group');
                return {
                    filters: {"customer_group": customer_group}
                };
            },
            on_change: () => {
				var customer = frappe.query_report.get_filter_value('customer');
				if (customer) {
					frappe.db.get_value('Customer', customer, ["customer_name"], function(value) {
						frappe.query_report.set_filter_value('customer_name', value["customer_name"]);
					});
				} else {
					frappe.query_report.set_filter_value('customer_name', "");
				}
			}
        },
        {
            "fieldname": "customer_name",
            "label": __("Customer Name"),
            "fieldtype": "Data",
             "hidden": 0,

        },
        {
            "fieldname": "vessel_code",
            "label": __("Vessel"),
            "fieldtype": "Link",
            "options": 'Vessel',
             on_change: () => {
				var vessel_code = frappe.query_report.get_filter_value('vessel_code');
				if (vessel_code) {
					frappe.db.get_value('Vessel', vessel_code, ["vessel_description"], function(value) {
						frappe.query_report.set_filter_value('vessel_name', value["vessel_description"]);
					});
				} else {
					frappe.query_report.set_filter_value('vessel_name', "");
				}
			}
        },
		{
            "fieldname": "vessel_name",
            "label": __("Vessel Name"),
            "fieldtype": "Data",
            "hidden":0
        },
        {
            "fieldname": "item_group",
            "label": __("Item Group"),
            "fieldtype": "Link",
            "options": 'Item Group'
        }
    ],

};





