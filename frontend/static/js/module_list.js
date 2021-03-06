const selectRegionPadding = {"left": 20, "right": 265 + 20};
const $oneSelectedTools = $(".one-selected-tools");
const $atLeastOneSelectedTools = $(".at-least-one-selected-tools");
const $editTool = $("#edit-tool");

var onSelectChangeHooks = [];

var onSelectChange = function() {
    const $selected = $(".selected");
    const selectedCount = $selected.length;

    if (selectedCount == 0) {
        $oneSelectedTools.hide();
        $atLeastOneSelectedTools.hide();
    } else if (selectedCount == 1) {
        $oneSelectedTools.show();
        $atLeastOneSelectedTools.show();
        $editTool.find("a").attr("href", $selected.data("ref") + "/!action:update/");
    } else if (selectedCount > 1) {
        $oneSelectedTools.hide();
        $atLeastOneSelectedTools.show();
    }

    onSelectChangeHooks.forEach(function(element, index, array) {
        element($selected, selectedCount);
    });
};

(function ($) {
    $selectable.disableSelection();
    $workRegion.disableSelection();
    $selectable.click(function (event) {

    if ($("tr.selected").length > 0)
        handleSelect($(this), event);
    });

    $selectable.mousedown(function (event) {
        if ($("tr.selected").length == 0)
            handleSelect($(this), event);
    });

    $atLeastOneSelectedTools.click(function(event) {
        executeActionWithConfirm(
            null,
            "delete",
            getSelectedItemsData(),
            _("Delete selected items?"),
            function() {
                $(".selected").remove();
            }
        );
        event.preventDefault();
    });

    // Deselect all items when click on free space
    $workRegion.click(function(event) {
        if ($(event.target).closest(".object-tools").length > 0)
            return;

        if ($(event.target).hasClass("selectable"))
            return;

        if ($(event.target).closest(".selectable").length > 0)
            return;

        $selectable.not(".selected-by-region").removeClass("selected");
        $selectable.removeClass("selected-by-region");
        onSelectChange();
    });
})(jQuery);
