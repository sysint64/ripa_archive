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
            const $selected = $(".selected");

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
                    if ($selected.length > 1)
                        break;

                    location.href = $selected.find("td").first().data("href") + "!action:rename/";
                    break;

                case "edit_permissions":
                    if ($selected.length > 1)
                        break;

                    location.href = $selected.find("td").first().data("href") + "!action:edit-permissions/";
                    break;

                case "update_status":
                    if ($selected.length > 1)
                        break;

                    location.href = $selected.find("td").first().data("href") + "!action:update-document-status/";
                    break;
            }
        },
        items: {
            "rename": {
                name: "Rename",
                icon: "edit",
                disabled: function() { return $(".selected").length != 1; }
            },
            "edit_permissions": {
                name: "Edit permissions",
                icon: "fa-key",
                disabled: function() { return $(".selected").length != 1; }
            },
            "update_status": {
                name: "Update status",
                // icon: "fa-check",
                disabled: function() {
                    const $selected = $(".selected");
                    return $selected.length != 1 || !$selected.hasClass("document");
                }
            },
            "sep": "-",
            "cut": {name: "Cut", icon: "cut"},
            "copy": {name: "Copy", icon: "copy"},
            "delete": {name: "Delete", icon: "delete"}
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
            "sep": "-",
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

    // Sorting
    $("th.sorting").click(function() {
        const direction = $(this).hasClass("asc") ? "desc" : "asc";
        const field = $(this).data("sort-field");

        executeAction(
            "documents",
            "sort-by",
            {
                "sort_by": field,
                "sort_direction": direction
            },
            function () {
                showWaitDialog();
                location.reload();
            }
        );
    });
})(jQuery);
