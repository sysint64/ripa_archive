(function ($) {
    $(".top_search .dropdown-menu a").click(function(event) {
        $(".top_search button.dropdown-toggle").html(
            $(this).text()+' <span class="caret"></span>'
        );

        $(".top_search input[name=place]").val($(this).data("place"));
        event.preventDefault();
    });
})(jQuery);
