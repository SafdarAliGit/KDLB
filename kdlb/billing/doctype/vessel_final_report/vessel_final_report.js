// Copyright (c) 2023, TechVentural and contributors
// For license information, please see license.txt


const obj = {}

frappe.ui.form.on("Vessel Final Report", {
    onload: function (frm) {

        if (frm.doc.__islocal) {

            frappe.db.get_single_value('Due Date Days', 'due_date_days')
                .then(function (value) {
                    if (value) {
                        var defaultDueDate = frappe.datetime.add_days(frappe.datetime.get_today(), value);
                        frm.set_value('due_date', defaultDueDate);
                    } else {
                        var defaultDueDate = frappe.datetime.add_days(frappe.datetime.get_today(), 45);
                        frm.set_value('due_date', defaultDueDate);
                    }
                }).catch(function (err) {
                frappe.throw("Error:", err);
            });

        }
    },

    arrival_date: function (frm) {
        if ((frm.doc.import_teus > 0) || (frm.doc.export_teus > 0)) {
            frm.set_value("nature_of_cargo", null);
        }
        obj['arrival_date'] = frm.doc.arrival_date;
    },
    nature_of_cargo: function (frm) {
        obj['nature_of_cargo'] = frm.doc.nature_of_cargo;
        frm.set_value("amount", 0);
        frm.set_value("amount_after_surcharge", 0);
        frm.set_value("import_teus", 0);
        if (frm.doc.arrival_date) {
            obj['arrival_date'] = frm.doc.arrival_date;
        } else {
            frappe.msgprint(__('Select Arrival Date First'));
        }

    },

    // import_teus: function (frm) {
    //     obj['import_teus'] = frm.doc.import_teus;
    //     frm.set_value('export_teus', 0);
    //     var nature_of_cargo = frm.doc.nature_of_cargo;
    //     if (nature_of_cargo) {
    //         frappe.call({
    //             method: 'kdlb.billing.doctype.bill_entry.bill_entry.fetch_cargo_rate',
    //             args: {
    //                 'item_group': frm.doc.item_group, "date": obj.arrival_date,
    //             },
    //             callback: function (r) {
    //                 if (!r.exc) {
    //                     console.log(r.message);
    //                     // var price = r.message.normal_rate;
    //                     // var total_teus = obj.import_teus + obj.export_teus;
    //                     // var amount = price * total_teus;
    //                     // var surcharge_rate = frm.doc.surcharge;
    //                     // var surcharge = amount * (surcharge_rate / 100);
    //                     // var amount_after_surcharge = amount + surcharge;
    //                     // frm.set_value("amount", amount);
    //                     // frm.set_value("rate", price);
    //                     // frm.set_value("amount_after_surcharge", amount_after_surcharge);
    //                 }
    //             }
    //         });
    //     } else {
    //         frappe.show_alert(__('Select Nature Of Cargo First'));
    //     }
    //
    //
    // },
    // export_teus: function (frm) {
    //     obj['export_teus'] = frm.doc.export_teus;
    //     var nature_of_cargo = frm.doc.nature_of_cargo;
    //     if (nature_of_cargo) {
    //         frappe.call({
    //             method: 'kdlb.billing.doctype.bill_entry.bill_entry.fetch_cargo_rate',
    //             args: {
    //                 'cargo_code': obj.nature_of_cargo, "date": obj.arrival_date
    //             },
    //             callback: function (r) {
    //                 if (!r.exc) {
    //                     var price = r.message.normal_rate;
    //                     var total_teus = obj.import_teus + obj.export_teus;
    //                     var amount = price * total_teus;
    //                     var surcharge_rate = frm.doc.surcharge;
    //                     var surcharge = amount * (surcharge_rate / 100);
    //                     var amount_after_surcharge = amount + surcharge;
    //                     frm.set_value("amount", amount);
    //                     frm.set_value("rate", price);
    //                     frm.set_value("amount_after_surcharge", amount_after_surcharge);
    //                 }
    //             }
    //         });
    //     } else {
    //         frappe.show_alert(__('Select Nature Of Cargo First'));
    //     }
    //
    //
    // },

    refresh(frm) {

        frm.set_value("bill_no", frm.doc.name);
        // OPENS LEDGER
        // if (frm.doc.docstatus > 0) {
        //     frm.add_custom_button(__('Accounting Ledger'), function () {
        //         frappe.route_options = {
        //             voucher_no: frm.doc.name,
        //             from_date: frm.doc.posting_date,
        //             to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
        //             company: frm.doc.company,
        //             group_by: "Group by Voucher (Consolidated)",
        //             show_cancelled_entries: frm.doc.docstatus === 2
        //         };
        //         frappe.set_route("query-report", "General Ledger");
        //     });
        // }
        // TO GENERATE CESS BILLS
        if (frm.doc.docstatus === 1 && frm.doc.status !== 'Closed') {
            // AGENT BILL GENERATION
            frm.add_custom_button(__('Generate Agent Bill'), function () {

                frappe.call({
                    method: 'kdlb.billing.doctype.vessel_final_report.vessel_final_report.submit_agent_invoice',
                    args: {
                        'source_name': frm.doc.name
                    },
                    callback: function (r) {
                        if (!r.exc) {
                            // frappe.model.sync(r.message);
                            frappe.show_alert("Invoice Created");
                        }
                    }
                });

            }).addClass("btn-primary");
            // STEVEDORE BILL GENERATION

            frm.add_custom_button(__('Generate Stevedore Bill'), function () {
                frappe.call({
                    method: 'kdlb.billing.doctype.vessel_final_report.vessel_final_report.submit_stevedore_invoice',
                    args: {
                        'source_name': frm.doc.name
                    },
                    callback: function (r) {
                        if (!r.exc) {
                            // frappe.model.sync(r.message);
                            frappe.show_alert("Invoice Created");
                        }
                    }
                });
                // frappe.call({
                //     method: 'kdlb.billing.doctype.stevedore_bill.stevedore_bill.save_stevedore_bill',
                //     args: {
                //         'source_name': frm.doc.name,
                //         'item_group': frm.doc.item_group,
                //         "date": frm.doc.arrival_date,
                //         "abbr_stevedore": frm.doc.abbr_stevedore,
                //     },
                //     callback: function (r) {
                //         if (!r.message.error) {
                //             if (r.message.saved) {
                //                 frappe.msgprint(r.message.saved);
                //             } else if (r.message.already_saved) {
                //                 frappe.msgprint(r.message.already_saved);
                //             }
                //             setTimeout(function (e) {
                //                 window.location.reload();
                //             }, 2000);
                //         } else {
                //             frappe.msgprint(__(r.message.error));
                //         }
                //     }
                // });
            }).addClass("btn-primary");
            // KPT BILL GENERATION

            frm.add_custom_button(__('Generate KPT Bill'), function () {
                frappe.call({
                    method: 'kdlb.billing.doctype.vessel_final_report.vessel_final_report.submit_kpt_invoice',
                    args: {
                        'source_name': frm.doc.name
                    },
                    callback: function (r) {
                        if (!r.exc) {
                            // frappe.model.sync(r.message);
                            frappe.show_alert("Invoice Created");
                        }
                    }
                });
                // frappe.call({
                //     method: 'kdlb.billing.doctype.kpt_bill.kpt_bill.save_kpt_bill',
                //     args: {
                //         'source_name': frm.doc.name,
                //         'item_group': frm.doc.item_group,
                //         "date": frm.doc.arrival_date,
                //         "abbr_kpt": frm.doc.abbr_kpt,
                //     },
                //     callback: function (r) {
                //         if (!r.message.error) {
                //             if (r.message.saved) {
                //                 frappe.msgprint(r.message.saved);
                //             } else if (r.message.already_saved) {
                //                 frappe.msgprint(r.message.already_saved);
                //             }
                //             setTimeout(function (e) {
                //                 window.location.reload();
                //             }, 2000);
                //         } else {
                //             frappe.msgprint(__(r.message.error));
                //         }
                //     }
                // });
            }).addClass("btn-primary");
        }

    },
    setup: function (frm) {

        frm.set_query("ships_agent", function () {
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

        frm.set_query("kpt", function () {
            return {
                filters: [
                    ["Customer", "customer_group", "in", ["KPT"]], ["Customer", "is_frozen", "in", [0]]
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

        frm.set_query('ships_agent', 'vessel_final_report_items', function (doc, cdt, cdn) {
            return {
                filters: [
                    ["Customer", "customer_group", "in", ["AGENT"]]
                ]
            };
        });


    }
});


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
    $('input[data-fieldname="import_teus"], input[data-fieldname="export_teus"],' +
        ' input[data-fieldname="tc_no"],input[data-fieldname="ships_agent"],input[data-fieldname="stevedore"],' +
        'input[data-fieldname="kpt"],input[data-fieldname="vessel_code"],input[data-fieldname="berth"],' +
        'input[data-fieldname="arrival_date"],input[data-fieldname="sail_on_date"],input[data-fieldname="nature_of_cargo"],' +
        'input[data-fieldname="due_date"],input[data-fieldname="posting_date"],select[data-fieldname="rate_type"]')
        .css("background-color", "#FFE4C4");

    $('input[data-fieldname="import_teus"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="import_teus"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="export_teus"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="export_teus"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="tc_no"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="tc_no"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="ships_agent"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="ships_agent"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="stevedore"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="stevedore"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="kpt"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="kpt"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="berth"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="berth"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="vessel_code"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="vessel_code"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="arrival_date"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="arrival_date"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="sail_on_date"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="sail_on_date"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="nature_of_cargo"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="nature_of_cargo"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="due_date"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="due_date"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('input[data-fieldname="posting_date"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('input[data-fieldname="posting_date"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });
    $('select[data-fieldname="rate_type"]').focus(function () {
        $(this).css("background-color", "#50C878");
    });
    $('select[data-fieldname="rate_type"]').blur(function () {
        $(this).css("background-color", "#FFE4C4");
    });


});