// Copyright (c) 2023, TechVentural and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cargo Rates", {
    refresh(frm) {
        frm.set_query('customer_group', function (frm) {
            return {
                filters: [
                    ["Customer Group", "customer_group_name", "in", ["AGENT","STEVEDORE","KPT"]]
                ]
            };
        });

           frm.set_query('item_group', 'cargo_rates_items', function (doc, cdt, cdn) {
            return {
                filters: [
                    ["Item Group", "item_group_name", "in", ["Cargo","Container"]]
                ]
            };
        });

    },
});
