$.fn.exist = function (elem) {
    return elem.length > 0;
};

$.fn.disableSelection = function () {
    return this.attr('unselectable', 'on').css('user-select', 'none').on('selectstart', false);
};

$.fn.isBefore = function (elem) {
    if (typeof(elem) == "string")
        elem = $(elem);

    return this.add(elem).index(elem) > 0;
};

var $workRegion = $(".right_col");
var $selectable = $(".selectable");

function getSelectedItemsData() {
    var results = {};

    $(".selected").each(function() {
        const key = $(this).data("group");

        if (results[key] == null)
            results[key] = [];

        results[key].push($(this).data("id"));
    });

    return results;
}

function executeAction(action, inputData, callback) {
    showWaitDialog();

    var url;
    const relativeActions = ["paste"];

    if (relativeActions.indexOf(action) !== -1) {
        url = "!action:" + action + "/";
    } else {
        url = "/documents/!action:" + action + "/";
    }

    $.ajax({
        url: url,
        data: $.toJSON(inputData),
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
            "Content-Type": "application/json"
        },
        method: "POST",
        dataType: "json",
        success: function() {
            hideWaitDialog();
            callback();
        },
        error: function(info) {
            hideWaitDialog();
            showErrorDialog(getAjaxTextError(info));
        }
    });
}

function executeActionWithConfirm(action, inputData, message, callback) {
    showYesNoDialog(message, function() {
        executeAction(action, inputData, callback);
    });
}

$(document).ready(function() {
    $(".data-link").click(function() {
        location.href = $(this).data("href");
    });

    $(".data-double-click-link").dblclick(function() {
        location.href = $(this).data("href");
    });
});
