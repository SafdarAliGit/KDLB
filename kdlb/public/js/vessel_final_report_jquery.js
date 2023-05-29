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