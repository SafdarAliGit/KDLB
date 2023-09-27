$(document).ready(function() {
    // Disable F12 key
    $(document).keydown(function(e) {
        if (e.keyCode == 123) {
            e.preventDefault();
        }
    });

    // Disable context menu
    $(document).on("contextmenu", function(e) {
        e.preventDefault();
    });
});
