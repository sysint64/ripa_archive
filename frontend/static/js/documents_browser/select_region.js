(function ($) {
    var $selectRegion = $("#select-region");
    var selectRegionCoords = null;

    $workRegion.mousedown(function(event) {
        var exludeSelectRegion = $(event.target).is("td") || $(event.target).is("tr");
        exludeSelectRegion = exludeSelectRegion || $(event.target).hasClass("exclude-select-region");
        exludeSelectRegion = exludeSelectRegion || $(event.target).closest(".exclude-select-region").length > 0;

        if (exludeSelectRegion) {
            selectRegionCoords = null;
            return;
        }

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
                const width = Math.abs(selectRegionCoords.x2 - selectRegionCoords.x1);
                return Math.min(width, $workRegion.width() - this.left() + 110 - selectRegionPadding.right);
            },
            height: function() {
                return Math.abs(selectRegionCoords.y2 - selectRegionCoords.y1);
            }
        };
    });

    $workRegion.mousemove(function(event) {
        if (selectRegionCoords == null) {
            $selectRegion.hide();
            return;
        }

        selectRegionCoords.x2 = event.pageX;
        selectRegionCoords.y2 = event.pageY;

        selectRegionCoords.x1 = Math.max(selectRegionCoords.x1, $workRegion.offset().left + selectRegionPadding.left);
        selectRegionCoords.x2 = Math.max(selectRegionCoords.x2, $workRegion.offset().left + selectRegionPadding.left);

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

        if (onSelectChange != null)
            onSelectChange();
    });

    $(window).mouseup(function() {
        $selectRegion.hide();
        selectRegionCoords = null;
        dragging = false;
    });
})(jQuery);
