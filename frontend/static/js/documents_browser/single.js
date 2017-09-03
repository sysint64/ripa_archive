(function ($) {
    $("#take-for-revision").click(function(event) {
        executeActionWithConfirm(
            null,
            "take-for-revision",
            null,
            _("Take this document for revision?"),
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });

    $("#accept-document").click(function(event) {
        executeActionWithConfirm(
            null,
            "accept-document",
            null,
            _("Accept new version of document?"),
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });

    $("#reject-document").click(function(event) {
        executeActionWithConfirm(
            null,
            "reject-document",
            null,
            _("Reject new version of document and revert previous?"),
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });

    const $toggleFollow = $("#toggle-follow");
    $toggleFollow.click(function(event) {
        executeAction(
            null,
            "toggle-follow",
            null,
            function () {
                const $icon = $toggleFollow.find("i");

                if ($icon.hasClass("fa-eye")) {
                    $icon.removeClass("fa-eye").addClass("fa-eye-slash");
                    $icon.attr("title", _("Do not follow"));
                } else {
                    $icon.removeClass("fa-eye-slash").addClass("fa-eye");
                    $icon.attr("title", _("Follow"));
                }
            }
        );

        event.preventDefault();
    });

    $(".revert-document").click(function(event) {
        executeActionWithConfirm(
            null,
            "revert-document",
            {
                "activity_id": $(this).data("activity-id")
            },
            _("Revert this version of document?"),
            function () {
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
