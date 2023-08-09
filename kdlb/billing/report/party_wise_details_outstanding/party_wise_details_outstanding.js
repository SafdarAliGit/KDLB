frappe.query_reports["Party Wise Details Outstanding"] = {
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
                    filters: { "is_group": 0 }
                };
            }
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
        },
        {
            "fieldname": "vessel_name",
            "label": __("Vessel Name"),
            "fieldtype": "Link",
            "options": "Vessel",
        }
    ]
};
