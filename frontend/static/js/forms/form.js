(function ($) {
    // $("select[multiple]").addClass("selectpicker").selectpicker();
    $("select").addClass("selectpicker").selectpicker();

    const $checkboxes = $("input[type=checkbox].form-control");

    $("input[type=checkbox].form-control").each(function() {
        const $fieldWrapper = $(this).parent(".field-wrapper");

        if ($fieldWrapper.length > 0)
            $fieldWrapper.addClass("checkbox-wrapper");
    });

    $checkboxes.each(function() {
        if ($(this).is(":checked")) {
            $(this).parent().addClass("checked");
        } else {
            $(this).parent().removeClass("checked");
        }
    });

    $checkboxes.change(function() {
        if ($(this).is(":checked")) {
            $(this).parent().addClass("checked");
        } else {
            $(this).parent().removeClass("checked");
        }
    });
})(jQuery);
