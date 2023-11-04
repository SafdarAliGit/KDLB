// Copyright (c) 2023, TechVentural and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tonnage Out Summary"] = {
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

            "label": __("Party Group"),
            "fieldname": "customer_group",
            "fieldtype": "Link",
            "options": "Customer Group",
            "get_query": function () {
                return {
                    filters: {"is_group": 0}
                };
            }
        },

    ],
};
