(function ($) {
    onSelectChangeHooks.push(function($selected, selectedCount) {
        if (selectedCount != 1)
            return;

        $("#profile-link").attr("href", $selected.data("ref") + "/");
    });
})(jQuery);
