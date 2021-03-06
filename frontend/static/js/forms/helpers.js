function getAjaxTextError(info) {
    switch (info.status) {
        case 400:
            return $.parseJSON(info.responseText)[0];

        case 403:
            return _("Permission denied");

        default:
            return _("Unexpected error (server respond with status code ") + info.status + ")";
    }
}

function validateApiForm($form) {
    var serialize;
    var ajaxData = {
        url: $form.data("validation"),
        method: 'POST',
        dataType: "json",

        success: function() {
            $form.trigger('submit', [true]);
        },
        error: function(info) {
            try {
                var json = $.parseJSON(info.responseText);
                var $errorBlock = null;

                $.each(json.errors, function () {
                    if ($errorBlock == null)
                        $errorBlock = $form.find("[data-name=" + this.key + "_error]");

                    $form.find("[data-name=" + this.key + "_error]").html(this.desc);
                    $form.find("[name=" + this.key + "]")
                        .addClass("error")
                        .closest(".form-group")
                        .addClass("error");
                });

                $('html, body').scrollTop($errorBlock.offset().top - 5);
                $form.trigger('on_error', [info.status]);
            } catch (e) {
                $form.trigger('on_error', [info.status]);
            }
        }
    };

    if ($form.attr("enctype") == "multipart/form-data") {
        serialize = new FormData($form[0]);
        ajaxData = Object.assign({
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            cache: false
        }, ajaxData);
    } else {
        serialize = $form.serialize()+"&form="+$(this).attr("id");
    }

    ajaxData["data"] = serialize;

    $form.find(".form-error").html("");
    $form.find(".error").removeClass("error");
    $form.find(".generic-errors").html("");

    $.ajax(ajaxData);
}

function ajaxFormSubmit(event, isValid) {
    if (isValid)
        return;

    validateApiForm($(this));
    event.preventDefault();
}

function attachCSRFToken(data) {
    data["csrfmiddlewaretoken"] = Cookies.get('csrftoken');
    return data;
}

$(document).ready(function() {
    $(".ajax-form").submit(ajaxFormSubmit);
});


// Преобразование данных form.serializeArray в Object
function objectifyForm(formArray) {
    var returnArray = {};
    for (var i = 0; i < formArray.length; i++) {
        returnArray[formArray[i]['name']] = formArray[i]['value'];
    }
    return returnArray;
}
