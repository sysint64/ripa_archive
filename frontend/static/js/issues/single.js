(function ($) {
    $(".start-issues-item").click(function(event) {
        executeActionWithConfirm(
            null,
            "start-working-on-item",
            {
                "id": $(this).data("id")
            },
            _("Start working on this item?"),
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });

    $(".finish-issues-item").click(function(event) {
        executeActionWithConfirm(
            null,
            "finish-working-on-item",
            {
                "id": $(this).data("id")
            },
            _("Finish working on this item?"),
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });

    $(".approve-issues-item").click(function(event) {
        executeActionWithConfirm(
            null,
            "approve-working-on-item",
            {
                "id": $(this).data("id")
            },
            _("Approve this item?"),
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });
})(jQuery);
