(function ($) {
    var $selectRegion = $("#select-region");
    var selectRegionCoords = null;

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

    $workRegion.mousemove(function(event) {
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
        dragging = false;
    });
})(jQuery);
