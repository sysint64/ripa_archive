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

    $(".pause-issues-item").click(function(event) {
        executeActionWithConfirm(
            null,
            "pause-working-on-item",
            {
                "id": $(this).data("id")
            },
            _("Pause working on this item?"),
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

    $(".confirm-issues-item").click(function(event) {
        executeActionWithConfirm(
            null,
            "confirm-item",
            {
                "id": $(this).data("id")
            },
            _("Confirm this item?"),
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });

    $(".reject-issues-item").click(function(event) {
        executeActionWithConfirm(
            null,
            "reject-working-on-item",
            {
                "id": $(this).data("id")
            },
            _("Reject this item?"),
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });

    $(".accept-remark").click(function(event) {
        const $conteiner = $(this).closest("li.remark-li");
        executeActionWithConfirm(
            null,
            "accept-remark",
            {
                "remark_id": $(this).data("remark-id")
            },
            _("Accept this remark?"),
            function () {
                $conteiner.find(".reviewer-tools, .editor-tools").hide();
                $conteiner.find(".remark").removeClass("finished").removeClass("rejected").addClass("accepted");
            }
        );

        event.preventDefault();
    });

    $(".reject-remark").click(function(event) {
        const href = $(this).attr("href");

        showYesNoDialog(_("Reject this remark, and write another one?"), function() {
            location.href = href;
        });

        event.preventDefault();
    });

    $(".mark-as-finished").click(function(event) {
        const $conteiner = $(this).closest("li.remark-li");
        executeActionWithConfirm(
            null,
            "mark-as-finished-remark",
            {
                "remark_id": $(this).data("remark-id")
            },
            _("Mark this remark as \"finished\" and send notification to reviewer?"),
            function () {
                $conteiner.find(".reviewer-tools, .editor-tools").hide();
                $conteiner.find(".remark").removeClass("rejected").addClass("finished");
            }
        );

        event.preventDefault();
    });
})(jQuery);
