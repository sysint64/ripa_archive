var permissionsFormsPrefixes = [];

(function ($) {
    const $blockPermission = $("#block-permissions");
    const permissionBlockHtml = $blockPermission.html();
    const $permissionBlockCursor = $("#permission-block-cursor");

    const formPrefix = "permission-block";
    var lastBlockNumber = 0;

    $blockPermission.remove();

    function putPermission() {
        lastBlockNumber += 1;
        const prefix = formPrefix + parseInt(lastBlockNumber);

        var $block = $("<div/>", {"class": "block permissions-block", "html": permissionBlockHtml, "data-prefix": prefix});
        const addPrefix = function(index, attr) { return prefix + "-" + attr; };
        $block.find("label").attr("for", addPrefix);
        $block.find("input,select,textarea").attr("name", addPrefix).attr("id", addPrefix);
        $block.find(".form-error").attr("data-name", addPrefix);
        $block.find("select[multiple]").addClass("selectpicker").selectpicker();

        $permissionBlockCursor.before($block);
        permissionsFormsPrefixes.push(prefix);
    }

    $(".add-permission-button").click(function() {
        putPermission();
        rebindEvents();
    });
})(jQuery);
