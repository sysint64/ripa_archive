(function ($) {
    $("select[multiple]").addClass("selectpicker").selectpicker();
    const $checkboxes = $("input[type=checkbox].form-control");

    $checkboxes.each(function() {
        if ($(this).is(":checked")) {
            $(this).parent("label").addClass("checked");
        } else {
            $(this).parent("label").removeClass("checked");
        }
    });

    $checkboxes.change(function() {
        if ($(this).is(":checked")) {
            $(this).parent("label").addClass("checked");
        } else {
            $(this).parent("label").removeClass("checked");
        }
    });
})(jQuery);
