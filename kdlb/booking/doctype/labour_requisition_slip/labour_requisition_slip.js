// Copyright (c) 2023, TechVentural and contributors
// For license information, please see license.txt

frappe.ui.form.on('Labour Requisition Slip', {
       setup: function (frm) {

        frm.set_query("shiping_agent", function () {
            return {
                filters: [
                    ["Customer", "customer_group", "in", ["AGENT"]], ["Customer", "is_frozen", "in", [0]]
                ]
            };
        });

        frm.set_query("stevedore", function () {
            return {
                filters: [
                    ["Customer", "customer_group", "in", ["STEVEDORE"]], ["Customer", "is_frozen", "in", [0]]
                ]
            };
        });

        frm.set_query("nature_of_cargo", function () {
            return {
                filters: [
                    ["Item", "item_group", "in", ["Container", 'Cargo']]
                ]
            };
        });

    },
    refresh: function (frm) {
        frm.set_value("requisition_no", frm.doc.name);
    },

    no_of_workers:function (frm){
        frm.set_value('total_workers', frm.doc.no_of_workers + frm.doc.no_of_tindal + frm.doc.no_of_carier + frm.doc.no_of_serang + frm.doc.no_of_winchman + frm.doc.no_of_keyman);
    },
    no_of_tindal:function (frm){
        frm.set_value('total_workers', frm.doc.no_of_workers + frm.doc.no_of_tindal + frm.doc.no_of_carier + frm.doc.no_of_serang + frm.doc.no_of_winchman + frm.doc.no_of_keyman);
    },
    no_of_carier:function (frm){
        frm.set_value('total_workers', frm.doc.no_of_workers + frm.doc.no_of_tindal + frm.doc.no_of_carier + frm.doc.no_of_serang + frm.doc.no_of_winchman + frm.doc.no_of_keyman);
    },
    no_of_serang:function (frm){
        frm.set_value('total_workers', frm.doc.no_of_workers + frm.doc.no_of_tindal + frm.doc.no_of_carier + frm.doc.no_of_serang + frm.doc.no_of_winchman + frm.doc.no_of_keyman);
    },
    no_of_winchman:function (frm){
        frm.set_value('total_workers', frm.doc.no_of_workers + frm.doc.no_of_tindal + frm.doc.no_of_carier + frm.doc.no_of_serang + frm.doc.no_of_winchman + frm.doc.no_of_keyman);
    },
    no_of_keyman:function (frm){
        frm.set_value('total_workers', frm.doc.no_of_workers + frm.doc.no_of_tindal + frm.doc.no_of_carier + frm.doc.no_of_serang + frm.doc.no_of_winchman + frm.doc.no_of_keyman);
    }
});
