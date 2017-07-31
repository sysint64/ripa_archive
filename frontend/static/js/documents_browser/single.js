(function ($) {
    $("#take-for-revision").click(function () {
        executeActionWithConfirm(
            null,
            "take-for-revision",
            {"id": 0},
            "Take this document for revision?",
            function () {
                showSuccessDialog("Took successfully");
            }
        );
    });
})(jQuery);
