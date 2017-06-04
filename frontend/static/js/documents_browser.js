(function ($) {
    var $selectable = $(".selectable");
    var $workRegion = $(".right_col");
    var $selectRegion = $("#select-region");

    $.fn.disableSelection = function() {
        return this.attr('unselectable', 'on').css('user-select', 'none').on('selectstart', false);
    };

    $.fn.isBefore = function (elem) {
        if (typeof(elem) == "string") elem = $(elem);
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
            copy: {name: "Copy", icon: "copy"},
            "paste": {name: "Paste", icon: "paste"},
            "delete": {name: "Delete", icon: "delete"},
            "sep1": "-",
            "quit": {
                name: "Quit", icon: function () {
                    return 'context-menu-icon context-menu-icon-quit';
                }
            }
        }
    });

    $.contextMenu({
        selector: '.right_col',
        callback: function (key, options) {
        },
        items: {
            "create_folder": {name: "Create folder", icon: "fa-file-o"},
            "create_document": {name: "Create document", icon: "fa-folder"}
        }
    });

    $selectable.bind("contextmenu", function() {
        $selectable.removeClass("selected");
        $(this).addClass("selected");
    });

    // TODO: need to refactor
    $selectable.click(function(event) {
        if (event.ctrlKey) {
            $(this).toggleClass("selected");
        } else if (event.shiftKey) {
            if ($lastSelected == null) {
                $selectable.removeClass("selected");
                $(this).addClass("selected");
            } else {
                var $firstElement, $lastElement;

                if ($lastSelected.isBefore($(this))) {
                    $firstElement = $lastSelected;
                    $lastElement = $(this);
                } else {
                    $firstElement = $(this);
                    $lastElement = $lastSelected;
                }

                $firstElement.nextUntil($lastElement).andSelf().add($lastElement).addClass("selected");
                $(this).addClass("selected");
            }
        } else {
            $selectable.removeClass("selected");
            $(this).addClass("selected");
        }

        if ($(this).hasClass("selected")) {
            $lastSelected = $(this);
        } else {
            $selectable.removeClass("selected");
            $lastSelected = null;
        }
    });

    // Deselect all items when click on free space
    $workRegion.click(function(event) {
        if ($(event.target).hasClass("selectable"))
            return;

        if ($(event.target).closest(".selectable").length > 0)
            return;

        $selectable.removeClass("selected");
        $lastSelected = null;
    });

    var selectRegionCoords = null;

    $workRegion.mousedown(function(event) {
        selectRegionCoords = {
            left: event.pageX,
            top: event.pageY,
            right: 0,
            bottom: 0
        };
    });

    $workRegion.mousemove(function() {
        if (selectRegionCoords == null) {
            $selectRegion.hide();
            return;
        }

        selectRegionCoords.right = event.pageX;
        selectRegionCoords.bottom = event.pageY;

        $selectRegion.show();
        $selectRegion.css("left", Math.min(selectRegionCoords.left, selectRegionCoords.right));
        $selectRegion.css("top", Math.min(selectRegionCoords.top, selectRegionCoords.bottom));
        $selectRegion.css("width", Math.abs(selectRegionCoords.right - selectRegionCoords.left));
        $selectRegion.css("height", Math.abs(selectRegionCoords.bottom - selectRegionCoords.top));
    });

    $(window).mouseup(function() {
        selectRegionCoords = null;
        $selectRegion.hide();
    });
})(jQuery);
