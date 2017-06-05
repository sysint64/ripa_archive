(function ($) {
    var $selectable = $(".selectable");
    var $workRegion = $(".right_col");
    var $selectRegion = $("#select-region");
    var selectRegionCoords = null;

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
            "copy": {name: "Copy", icon: "copy"},
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

        $selectable.not(".selected-by-region").removeClass("selected");
        $selectable.removeClass("selected-by-region");
        $lastSelected = null;
    });

    $workRegion.mousedown(function(event) {
        selectRegionCoords = {
            x1: event.pageX,
            y1: event.pageY,
            x2: 0,
            y2: 0,
            left: function() {
                return Math.min(selectRegionCoords.x1, selectRegionCoords.x2);
            },
            top: function() {
                return Math.min(selectRegionCoords.y1, selectRegionCoords.y2);
            },
            width: function() {
                return Math.abs(selectRegionCoords.x2 - selectRegionCoords.x1);
            },
            height: function() {
                return Math.abs(selectRegionCoords.y2 - selectRegionCoords.y1);
            }
        };
    });

    $workRegion.mousemove(function() {
        if (selectRegionCoords == null) {
            $selectRegion.hide();
            return;
        }

        selectRegionCoords.x2 = event.pageX;
        selectRegionCoords.y2 = event.pageY;

        if (selectRegionCoords.width() < 10 && selectRegionCoords.height() < 10)
            return;

        $selectRegion.show();
        $selectRegion.css("left", selectRegionCoords.left());
        $selectRegion.css("top", selectRegionCoords.top());
        $selectRegion.css("width", selectRegionCoords.width());
        $selectRegion.css("height", selectRegionCoords.height());

        $selectable.each(function() {
            const top = $(this).offset().top;
            const height = $(this).height();

            // test element in rect
            if (top + height >= selectRegionCoords.top() && top <= selectRegionCoords.top() + selectRegionCoords.height()) {
                $(this).addClass("selected").addClass("selected-by-region");
            } else {
                $(this).removeClass("selected").removeClass("selected-by-region");
            }
        });
    });

    $(window).mouseup(function() {
        $selectRegion.hide();
        selectRegionCoords = null;
    });
})(jQuery);
