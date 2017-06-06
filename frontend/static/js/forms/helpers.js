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

            $.each(json.errors, function () {
                $form.find("[data-name="+this.key+"_error]").html(this.desc);
                $form.find("[name="+this.key+"]").closest(".form-group").addClass("error");
            });
        }
    });
}

function ajaxFormSubmit(e, isValid) {
    if (isValid) {
        if ($(this).data("refresh") === "true")
            window.location.reload();

        return;
    }

    validateApiForm($(this));
    e.preventDefault();
}

function attach_csrf_token(data) {
    data["csrfmiddlewaretoken"] = $("input[name=csrfmiddlewaretoken]:first").val();
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
