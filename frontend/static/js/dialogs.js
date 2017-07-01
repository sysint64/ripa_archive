const $errorDialog = $("#error-dialog");
const $errorDialogText = $errorDialog.find(".content");
const $waitDialog = $("#wait-dialog");
const $yesNoDialog = $("#yes-no-dialog");
const $yesNoDialogYesButton = $yesNoDialog.find("button.primary");
const $yesNoDialogText = $yesNoDialog.find(".content");

function showErrorDialog(message) {
    $errorDialog.show();
    $errorDialogText.html(message);
}

function showWaitDialog() {
    $waitDialog.show();
}

function hideWaitDialog() {
    $waitDialog.hide();
}

function showYesNoDialog(message, callback) {
    $yesNoDialog.show();
    $yesNoDialogText.html(message);
    $yesNoDialogYesButton.unbind("click");
    $yesNoDialogYesButton.click(function() {
        callback();
        $yesNoDialog.hide();
    });
}

(function ($) {
    $(".close-dialog").click(function() {
        $(this).closest(".dialog").hide();
    });
})(jQuery);
