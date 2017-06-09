(function ($) {
    var delta = 0;
    var clickOffset = 0;
    var $dragRegion = $("#drag-region");
    var clicked = false;
    var regionHeight = 0;
    var regionPivotOffset = 0;
    var preventDragging = false;
    var preventAction = false;

    $workRegion.mousedown(function(event) {
        clickOffset = event.pageY;
        clicked = true;
        var selectedOffset = 0;

        if ($("tr.selected").length > 0) {
            selectedOffset = $("tr.selected:first").offset().top;
        }

        regionPivotOffset = clickOffset - selectedOffset;

        if (!$(event.target).is("td"))
            preventDragging = true;
    });

    $workRegion.mousemove(function(event) {
        if (!clicked || preventDragging) {
            $dragRegion.hide();
            return;
        }

        delta = event.pageY - clickOffset;

        if (Math.abs(delta) < 20) {
            $dragRegion.hide();
            return;
        }

        const $selected = $("tr.selected");
        regionHeight = $selected.height() * $selected.length;

        $dragRegion.show();
        $dragRegion.css("height", regionHeight);
        $dragRegion.css("width", $workRegion.width());
        $dragRegion.css("left", $workRegion.offset().left + 20);
        $dragRegion.css("top", event.pageY - regionPivotOffset);

        dragging = true;
        $selected.addClass("targeted");

        $selectable.not(".targeted").each(function() {
            const top = $(this).offset().top;
            const height = $(this).height();
            const cursor = event.pageY;

            if (top <= cursor && top + height >= cursor) {
                $(".to_folder").removeClass("to_folder");
                $(this).addClass("to_folder");
            } else {
                $(this).removeClass("to_folder");
            }
        });
    });

    function mouseUpHandle(event) {
        preventDragging = false;
        const $toFolder = $(".to_folder");
        const $targeted = $(".targeted");

        resetState = function() {
            clicked = false;
            dragging = false;
            $dragRegion.hide();

            $targeted.removeClass("targeted");
            $toFolder.removeClass("to_folder");
        };

        function serialize($items, dataName) {
            var result = [];

            $items.each(function() {
                result.push($(this).data(dataName));
            });

            return result;
        }

        if ($toFolder.length == 1) {
            const inputData = {
                "to_folder": $toFolder.data("folder-id"),
                "folders": serialize($targeted.not(".document"), "folder-id"),
                "documents": serialize($targeted.not(".folder"), "document-id")
            };

            resetState();

            if (preventAction) {
                preventAction = false;
                return;
            }

            executeAction("change-folder", inputData, function() {
                $targeted.remove();
            });
        } else {
            resetState();
        }
    }

    $workRegion.mouseup(mouseUpHandle);

    $(document).keydown(function(event) {
        if (event.which == 27) {
            preventAction = true;
            mouseUpHandle(event);
            preventMouseUp = true;
        }
    });
})(jQuery);
