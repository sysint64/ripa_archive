(function ($) {
    const $blockPermission = $("#block-permissions");
    const permissionBlockHtml = $blockPermission.html();
    const $permissionBlockCursor = $("#permission-block-cursor");

    function putPermission() {
        const prefix = "";
        var $block = $("<div/>", {"class": "block", "html": permissionBlockHtml, "data-prefix": prefix});
        const addPrefix = function(index, attr) { return prefix + "-" + attr; };
        // $block.find("label").attr("for", addPrefix);
        // $block.find("input").attr("name", addPrefix).attr("id", addPrefix);
        // $block.find(".form-error").attr("data-name", addPrefix);
        $permissionBlockCursor.before($block);
    }

    $(".add-permission-button").click(function() {
        putPermission();
        rebindEvents();
    });

    $("input[type=checkbox].form-control").change(function() {
        if ($(this).is(":checked")) {
            $(this).parent("label").addClass("checked");
        } else {
            $(this).parent("label").removeClass("checked");
        }
    });
})(jQuery);
