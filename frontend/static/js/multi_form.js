(function ($) {
    $("input").addClass("form-control");
    $(".add-block-button").click(function() {
        $(".multi-form").find(".block").removeClass("active");
        $("#block-cursor").before($("#block-template").html());

        $(".block").unbind("click");

        $(".block").click(function() {
            $(".multi-form").find(".block").removeClass("active");
            $(this).addClass("active");
        });
    });

    $(".block").click(function() {
        $(".multi-form").find(".block").removeClass("active");
        $(this).addClass("active");
    });

    $("input").focus(function() {
        $(".multi-form").find(".block").removeClass("active");
        $(this).closest(".block").addClass("active");
    });
})(jQuery);
