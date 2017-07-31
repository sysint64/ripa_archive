function bindEvents() {
    $(".block").click(function() {
        $(".multi-form").find(".block").removeClass("active");
        $(this).addClass("active");
    });

    $(".remove-block").click(function() {
        const $block = $(this).closest(".block");
        const index = formsPrefixes.indexOf($block.data("prefix"));
        formsPrefixes.splice(index, 1);
        console.log(formsPrefixes);
        $(this).closest(".block").remove();
    });

    $("input[type=checkbox].form-control").change(function() {
        if ($(this).is(":checked")) {
            $(this).parent("label").addClass("checked");
        } else {
            $(this).parent("label").removeClass("checked");
        }
    });
}

function unbindEvents() {
    $(".block").unbind("click");
    $(".remove-block").unbind("click");
    $("input[type=checkbox].form-control").unbind("change");
}

function rebindEvents() {
    unbindEvents();
    bindEvents();
}

(function ($) {
    $("input").addClass("form-control");
    const $blockPrimary = $("#block-primary");
    const primaryBlockHtml = $blockPrimary.html();
    const formPrefix = "block";
    var lastBlockNumber = 0;
    var formsPrefixes = [];

    $blockPrimary.find(".remove-block").remove();

    function putBlock() {
        lastBlockNumber += 1;
        const prefix = formPrefix + parseInt(lastBlockNumber);

        var $block = $("<div/>", {"class": "block", "html": primaryBlockHtml, "data-prefix": prefix});
        const addPrefix = function(index, attr) { return prefix + "-" + attr; };
        $block.find("label").attr("for", addPrefix);
        $block.find("input,select").attr("name", addPrefix).attr("id", addPrefix);
        $block.find(".form-error").attr("data-name", addPrefix);
        $("#block-cursor").before($block);

        formsPrefixes.push(prefix);
        console.log(formsPrefixes);
    }

    $(".add-block-button").click(function() {
        putBlock();
        rebindEvents();
    });

    $("#multiform").submit(function(event, isValid) {
        showWaitDialog();
        $(this).find("#form_prefixes").val(formsPrefixes.join(","));

        if ($(this).find("#permissions_form_prefixes").length > 0)
            $(this).find("#permissions_form_prefixes").val(permissionsFormsPrefixes.join(","));

        if (isValid) {
            return;
        }

        event.preventDefault();
        validateApiForm($(this));
    });

    $("#multiform").on("validation_error", function() {
        hideWaitDialog();
    });

    bindEvents();
})(jQuery);
