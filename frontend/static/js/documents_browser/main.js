var dragging = false;
var preventMouseUp = false;
var selectRegionPadding = {"left": 20, "right": 20};
var onSelectChange = null;

(function ($) {
    $selectable.disableSelection();
    $workRegion.disableSelection();

    var $lastSelected = null;

    $.contextMenu({
        selector: '.context-menu',
        callback: function (key, options) {
            switch (key) {
                case "delete":
                    executeActionWithConfirm(
                        "documents",
                        "delete",
                        getSelectedItemsData(),
                        "Delete selected items?",
                        function() {
                            $(".selected").remove();
                        }
                    );
                    break;

                case "copy":
                    executeAction(
                        "documents",
                        "copy",
                        getSelectedItemsData(),
                        function() {}
                    );
                    break;

                case "cut":
                    executeAction(
                        "documents",
                        "cut",
                        getSelectedItemsData(),
                        function() {
                            $(".selected").addClass("cut").removeClass("selected");
                        }
                    );
                    break;

                case "rename":
                    const $selected = $(".selected");

                    if ($selected.length > 1)
                        break;

                    location.href = $selected.find("td").first().data("href") + "!action:rename/";
                    break
            }
        },
        items: {
            "edit": {name: "Edit", icon: "edit"},
            "cut": {name: "Cut", icon: "cut"},
            "copy": {name: "Copy", icon: "copy"},
            "delete": {name: "Delete", icon: "delete"},
            "rename": {name: "Rename", icon: "rename"}
        },
        events: {
            show: function(options) {
                dragClicked = false;
            }
        }
    });

    $.contextMenu({
        selector: '.right_col',
        callback: function (key, options) {
            switch (key) {
                case "create_folders":
                    location.href = "!action:create-folders/";
                    break;

                case "create_documents":
                    location.href = "!action:create-documents/";
                    break;

                case "paste":
                    executeAction(
                        "documents",
                        "paste",
                        {},
                        function() {
                            showWaitDialog();
                            location.reload();
                        });
                    break;
            }
        },
        items: {
            "create_folders": {name: "Create folder(s)", icon: "fa-folder"},
            "create_documents": {name: "Create document(s)", icon: "fa-file-o"},
            "paste": {name: "Paste", icon: "paste"}
        },
        events: {
            show: function(options) {
                dragClicked = false;
            }
        }
    });

    $selectable.bind("contextmenu", function() {
        if (!$(this).hasClass("selected")) {
            $selectable.removeClass("selected");
            $(this).addClass("selected");
        }
    });

    $selectable.click(function(event) {
        if ($("tr.selected").length > 0)
            handleSelect($(this), event);
    });

    $selectable.mousedown(function(event) {
        if ($("tr.selected").length == 0)
            handleSelect($(this), event);
    });

    // Deselect all items when click on free space
    $workRegion.click(function(event) {
        if (preventMouseUp) {
            preventMouseUp = false;
            return;
        }

        if (dragging)
            return;

        if ($(event.target).hasClass("selectable"))
            return;

        if ($(event.target).closest(".selectable").length > 0)
            return;

        $selectable.not(".selected-by-region").removeClass("selected");
        $selectable.removeClass("selected-by-region");
        $lastSelected = null;

        if (onSelectChange != null)
            onSelectChange();
    });
})(jQuery);
