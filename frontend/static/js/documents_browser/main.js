var dragging = false;
var preventMouseUp = false;
var selectRegionPadding = {"left": 20, "right": 20};
var onSelectChange = null;

(function ($) {
    $selectable.disableSelection();
    $workRegion.disableSelection();

    const $parentFolderPermissions = $("#parent-folder-perms");
    var $lastSelected = null;

    function parsePermissions($item) {
        const permissions = $item.data("permissions");
        const permissionsArray = permissions.split(";");

        var map = {};

        permissionsArray.forEach(function callback(currentValue, index, array) {
            const permission = currentValue.split(":");
            map[permission[0]] = permission[1] === "1";
        });

        return map;
    }

    function contextMenuItemIsDisabled($item, perm) {
        if ($item.length != 1)
            return true;

        const permissions = parsePermissions($item);
        return !permissions[perm];
    }

    function contextMenuItemIsBulkDisabled($item, perm) {
        const permissions = parsePermissions($item);
        return !permissions[perm];
    }

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
                disabled: function() { return contextMenuItemIsDisabled($(".selected"), "edit"); }
            },
            "edit_permissions": {
                name: "Edit permissions",
                icon: "fa-key",
                disabled: function() { return contextMenuItemIsDisabled($(".selected"), "edit_permissions"); }
            },
            "update_status": {
                name: "Update status",
                // icon: "fa-check",
                disabled: function() { return contextMenuItemIsDisabled($(".selected"), "edit"); }
            },
            "sep": "-",
            "cut": {
                name: "Cut",
                icon: "cut",
                disabled: function () { return contextMenuItemIsBulkDisabled($(".selected"), "edit"); }
            },
            "copy": {
                name: "Copy",
                icon: "copy",
                disabled: function () { return contextMenuItemIsBulkDisabled($(".selected"), "edit"); }
            },
            "delete": {
                name: "Delete",
                icon: "delete",
                disabled: function () { return contextMenuItemIsBulkDisabled($(".selected"), "delete"); }
            }
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
            "create_folders": {
                name: "Create folder(s)",
                icon: "fa-folder",
                disabled: function () { return contextMenuItemIsDisabled($parentFolderPermissions, "create_folders"); }
            },
            "create_documents": {
                name: "Create document(s)",
                icon: "fa-file-o",
                disabled: function () { return contextMenuItemIsDisabled($parentFolderPermissions, "create_documents"); }
            },
            "sep": "-",
            "paste": {
                name: "Paste", icon: "paste",
                disabled: function () { return contextMenuItemIsDisabled($parentFolderPermissions, "edit"); }
            }
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
