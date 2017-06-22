function ajaxErrorHandler(info, selector) {
    if (info.status >= 500) {
        $(selector).html("Неизвестная ошибка");
        setTimeout(function () {
            $(selector).html("");
        }, 5000);
    } else {
        var data = $.parseJSON(info.responseText);
        $(selector).html(data.error);
        setTimeout(function () {
            $(selector).html("");
        }, 5000);
    }
}

function validateApiForm($form) {
    var serialize = $form.serialize()+"&form="+$(this).attr("id");
    $form.find(".form-error").html("");
    $form.find(".error").removeClass("error");
    $form.find(".generic-errors").html("");

    $.ajax({
        url: $form.data("validation"),
        data: serialize,
        method: 'POST',
        dataType: "json",
        success: function() {
            $form.trigger('submit', [true]);
        },
        error: function(info) {
            var json = $.parseJSON(info.responseText);
            var $errorBlock = null;

            $.each(json.errors, function () {
                if ($errorBlock == null)
                    $errorBlock = $form.find("[data-name="+this.key+"_error]");

                $form.find("[data-name="+this.key+"_error]").html(this.desc);
                $form.find("[name="+this.key+"]")
                    .addClass("error")
                    .closest(".form-group")
                    .addClass("error");
            });

            $('html, body').scrollTop($errorBlock.offset().top - 5);
        }
    });
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
