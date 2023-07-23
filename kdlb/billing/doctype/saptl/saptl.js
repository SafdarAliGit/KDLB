// Copyright (c) 2023, TechVentural and contributors
// For license information, please see license.txt


$(document).ready(function () {
// FUNCTION TO ADD TAB INDEX AND NAVIGATE TO ON ENTER KEY
    $(function () {
        var tabindex = 1;
        $('input,select').each(function () {
            if (this.type != "hidden") {
                var $input = $(this);
                $input.attr("tabindex", tabindex);
                tabindex++;
            }
        });

        $('input,select').on('keypress', function (e) {
            e.which !== 13 || $('[tabIndex=' + (+this.tabIndex + 1) + ']')[0].focus();
        });
    });
// =====================

    $('input[data-fieldname="arrival_date"],input[data-fieldname="vessel_code"],input[data-fieldname="customer"]')
        .css("background-color", "#FFE4C4");

    $('input[data-fieldname="arrival_date"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="arrival_date"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });


    $('input[data-fieldname="vessel_code"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="vessel_code"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });

    $('input[data-fieldname="customer"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="customer"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });

});


function calculate_totals(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    var total_amount = 0;
    var total_import_teus = 0;
    var total_export_teus = 0;
    $.each(frm.doc.saptl_items || [], function (i, d) {
        total_amount += flt(d.amount);
        total_import_teus += flt(d.import_teus);
        total_export_teus += flt(d.export_teus);
    });
    frm.set_value("total_amount", total_amount);
    frm.set_value("total_import_teus", total_import_teus);
    frm.set_value("total_export_teus", total_export_teus);

}

frappe.ui.form.on('Saptl', {


    fetch_items: function (frm) {
        if (frm.doc.docstatus == 0) {
            frappe.call({
                method: "kdlb.billing.doctype.saptl.saptl.get_items",
            }).done((r) => {

                frm.doc.saptl_items = [];

                $.each(r.message, function (_i, e) {
                    let entry = frm.add_child("saptl_items");
                    entry.item = e.cargo_code;
                    entry.rate = e.rate;
                })
                refresh_field("saptl_items");

            })
        }
    },
    refresh(frm) {

        frm.set_df_property("saptl_items", 'cannot_add_rows', true);
        // frm.set_df_property("saptl_items", 'cannot_delete_rows', true);

        frm.set_value("bill_no", frm.doc.name);
        frm.set_query('item', 'saptl_items', function (doc, cdt, cdn) {
            return {
                filters: [
                    ["Item", "item_group", "in", ["SAPTL"]]
                ]
            };
        });
        frm.set_query('customer', function (doc, cdt, cdn) {
            return {
                filters: [

                    ["Customer", "customer_group", "in", ["SAPTL"]]
                ]
            };
        });


        if (frm.doc.docstatus > 0) {
            frm.add_custom_button(__('Accounting Ledger'), function () {
                frappe.route_options = {
                    voucher_no: frm.doc.name,
                    from_date: frm.doc.posting_date,
                    to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
                    company: frm.doc.company,
                    group_by: "Group by Voucher (Consolidated)",
                    show_cancelled_entries: frm.doc.docstatus === 2
                };
                frappe.set_route("query-report", "General Ledger");
            }, __("View"));
        }

    },


});


frappe.ui.form.on('Saptl Items', {


    export_teus: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var import_teus = d.import_teus;
        var export_teus = d.export_teus;
        var total = import_teus + export_teus;
        frappe.model.set_value(cdt, cdn, "total", total);
        var amount = d.rate * total;
        frappe.model.set_value(cdt, cdn, "amount", amount);
        calculate_totals(frm, cdt, cdn);
    },
    import_teus: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var import_teus = d.import_teus;
        var export_teus = d.export_teus;
        var total = import_teus + export_teus;
        frappe.model.set_value(cdt, cdn, "total", total);
        var amount = d.rate * total;
        frappe.model.set_value(cdt, cdn, "amount", amount);
        calculate_totals(frm, cdt, cdn);
    },

    item: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var nature_of_cargo = d.item;
        if (nature_of_cargo) {
            frappe.call({
                method: 'kdlb.billing.doctype.saptl.saptl.fetch_saptl_rate',
                args: {
                    'cargo_code': nature_of_cargo,
                },
                callback: function (r) {
                    if (!r.exc) {
                        var rate = r.message.rate;
                        frappe.model.set_value(cdt, cdn, "rate", rate);
                    }
                }
            });
        } else {
            frappe.show_alert(__('Select Item First'));
        }

    }
})