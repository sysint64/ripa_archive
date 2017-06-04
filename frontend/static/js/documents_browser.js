(function ($) {
    $.fn.disableSelection = function() {
        return this.attr('unselectable', 'on').css('user-select', 'none').on('selectstart', false);
    };
    $.fn.isBefore = function (elem) {
        if (typeof(elem) == "string") elem = $(elem);
        return this.add(elem).index(elem) > 0;
    };

    $('.selectable').disableSelection();

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

    $(".selectable").click(function(event) {
        if (event.ctrlKey) {
            $(this).toggleClass("selected");
        } else if (event.shiftKey) {
            if ($lastSelected == null) {
                $(".selectable").removeClass("selected");
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
            $(".selectable").removeClass("selected");
            $(this).addClass("selected");
        }

        if ($(this).hasClass("selected")) {
            $lastSelected = $(this);
        } else {
            $(".selectable").removeClass("selected");
            $lastSelected = null;
        }
    });

    // Deselect all items when click on free space
    $(".right_col").click(function(event) {
        if ($(event.target).hasClass("selectable"))
            return;

        if ($(event.target).closest(".selectable").length > 0)
            return;

        $(".selectable").removeClass("selected");
        $lastSelected = null;
    });
})(jQuery);
