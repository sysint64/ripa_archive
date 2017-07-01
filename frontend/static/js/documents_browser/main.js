var $workRegion = $(".right_col");
var $selectable = $(".selectable");
var dragging = false;
var preventMouseUp = false;

function getDocumentsIds() {

}

function executeAction(action, inputData, callback) {
    showWaitDialog();

    $.ajax({
        url: "/documents/!action:" + action + "/",
        data: $.toJSON(inputData),
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
            "Content-Type": "application/json"
        },
        method: "POST",
        dataType: "json",
        success: function() {
            hideWaitDialog();
            callback();
        },
        error: function(info) {
            hideWaitDialog();
            showErrorDialog(getAjaxTextError(info));
        }
    });
}

function executeActionWithConfirm(action, inputData, message, callback) {
    showYesNoDialog(message, function() {
        executeAction(action, inputData, callback);
    });
}

(function ($) {
    $.fn.disableSelection = function() {
        return this.attr('unselectable', 'on').css('user-select', 'none').on('selectstart', false);
    };

    $.fn.isBefore = function (elem) {
        if (typeof(elem) == "string")
            elem = $(elem);

        return this.add(elem).index(elem) > 0;
    };

    $selectable.disableSelection();
    $workRegion.disableSelection();

    var $lastSelected = null;

    $.contextMenu({
        selector: '.context-menu',
        callback: function (key, options) {
        },
        items: {
            "edit": {name: "Edit", icon: "edit"},
            "cut": {name: "Cut", icon: "cut"},
            "copy": {name: "Copy", icon: "copy"},
            "paste": {name: "Paste", icon: "paste"},
            "delete": {name: "Delete", icon: "delete"}
        }
    });

    $.contextMenu({
        selector: '.right_col',
        callback: function (key, options) {
            switch (key) {
                case "create_folders": location.href = "!action:create-folders/"; break;
                case "create_documents": location.href = "!action:create-documents/"; break;
            }
        },
        items: {
            "create_folders": {name: "Create folder(s)", icon: "fa-folder"},
            "create_documents": {name: "Create document(s)", icon: "fa-file-o"}
        }
    });

    $selectable.bind("contextmenu", function() {
        if (!$(this).hasClass("selected")) {
            $selectable.removeClass("selected");
            $(this).addClass("selected");
        }
    });

    // TODO: need to refactor
    function handleSelect($this, event) {
        if (event.ctrlKey) {
            $this.toggleClass("selected");
        } else if (event.shiftKey) {
            if ($lastSelected == null) {
                $selectable.removeClass("selected");
                $this.addClass("selected");
            } else {
                var $firstElement, $lastElement;

                if ($lastSelected.isBefore($this)) {
                    $firstElement = $lastSelected;
                    $lastElement = $this;
                } else {
                    $firstElement = $this;
                    $lastElement = $lastSelected;
                }

                $firstElement.nextUntil($lastElement).andSelf().add($lastElement).addClass("selected");
                $this.addClass("selected");
            }
        } else {
            $selectable.removeClass("selected");
            $this.addClass("selected");
        }

        if ($this.hasClass("selected")) {
            $lastSelected = $this;
        } else {
            $selectable.removeClass("selected");
            $lastSelected = null;
        }
    }

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
    });
})(jQuery);
