
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
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "get_query": function () {
                var customer_group = frappe.query_report.get_filter_value('customer_group');
                return {
                    filters: {"customer_group": customer_group}
                };
            }
        },
        {
            "fieldname": "vessel_code",
            "label": __("Vessel"),
            "fieldtype": "Link",
            "options": 'Vessel'
        },
		{
            "fieldname": "item_group",
            "label": __("Item Group"),
            "fieldtype": "Link",
            "options": 'Item Group'
        }
    ],

};
