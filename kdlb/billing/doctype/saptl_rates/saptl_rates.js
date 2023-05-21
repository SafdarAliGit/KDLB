// Copyright (c) 2023, TechVentural and contributors
// For license information, please see license.txt

frappe.ui.form.on("Saptl Rates", {
    refresh(frm) {
        frm.set_query('cargo_code', function (doc, cdt, cdn) {
            return {
                filters: [
                    ["Item", "item_group", "in", ["SAPTL"]]
                ]
            };
        });

    },
});

