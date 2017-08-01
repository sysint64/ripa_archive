(function ($) {
    $("#take-for-revision").click(function (event) {
        executeActionWithConfirm(
            null,
            "take-for-revision",
            {"id": 0},
            "Take this document for revision?",
            function () {
                showWaitDialog();
                location.reload();
            }
        );

        event.preventDefault();
    });
})(jQuery);
