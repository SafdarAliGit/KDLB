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

});

frappe.ui.form.on('Labour Requisition Slip Item', {

    workers: function (frm, cdt, cdn) {
        var total_workers = 0;
        var d = locals[cdt][cdn];
        total_workers = d.workers + d.tindal + d.carier + d.serang + d.winchman + d.keyman;
        frappe.model.set_value(cdt, cdn,'total_workers',d.gangs * total_workers);
    },
    tindal: function (frm, cdt, cdn) {
        var total_workers = 0;
        var d = locals[cdt][cdn];
        total_workers = d.workers + d.tindal + d.carier + d.serang + d.winchman + d.keyman;
        frappe.model.set_value(cdt, cdn,'total_workers', d.gangs * total_workers);
    },
    carier: function (frm, cdt, cdn) {
        var total_workers = 0;
        var d = locals[cdt][cdn];
        total_workers = d.workers + d.tindal + d.carier + d.serang + d.winchman + d.keyman;
        frappe.model.set_value(cdt, cdn,'total_workers',  d.gangs * total_workers);
    },
    serang: function (frm, cdt, cdn) {
        var total_workers = 0;
        var d = locals[cdt][cdn];
        total_workers = d.workers + d.tindal + d.carier + d.serang + d.winchman + d.keyman;
        frappe.model.set_value(cdt, cdn,'total_workers',  d.gangs * total_workers);
    },
    winchman: function (frm, cdt, cdn) {
        var total_workers = 0;
        var d = locals[cdt][cdn];
        total_workers = d.workers + d.tindal + d.carier + d.serang + d.winchman + d.keyman;
        frappe.model.set_value(cdt, cdn,'total_workers',  d.gangs * total_workers);
    },
    keyman: function (frm, cdt, cdn) {
        var total_workers = 0;
        var d = locals[cdt][cdn];
        total_workers = d.workers + d.tindal + d.carier + d.serang + d.winchman + d.keyman;
        frappe.model.set_value(cdt, cdn,'total_workers',  d.gangs * total_workers);
    },
    gangs: function (frm, cdt, cdn) {
        var total_workers = 0;
        var d = locals[cdt][cdn];
        total_workers = d.workers + d.tindal + d.carier + d.serang + d.winchman + d.keyman;
        frappe.model.set_value(cdt, cdn,'total_workers',  d.gangs * total_workers);
    }

});

