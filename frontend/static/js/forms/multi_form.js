var formsPrefixes = [];
var deleteIds = [];

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
        const $instanceIdInput = $block.find("input[type=hidden].instance-id");

        if ($instanceIdInput.length > 0)
            deleteIds.push($instanceIdInput.val());

        console.log(deleteIds);
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

    $blockPrimary.remove();

    $(".block").each(function() {
        if (typeof $(this).data("prefix") === "undefined" || $(this).data("prefix") === "")
            return;

        const prefix = $(this).data("prefix");

        lastBlockNumber += 1;
        formsPrefixes.push(prefix);
    });

    console.log(formsPrefixes);

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

    function putFirstBlock() {
        var $block = $("<div/>", {"class": "block", "html": primaryBlockHtml});
        $("#block-cursor").before($block);
    }

    $(".add-block-button").click(function() {
        if ($(".block").length == 0) {
            putFirstBlock();
        } else {
            putBlock();
        }

        rebindEvents();
    });

    const $multiform = $("#multiform");

    $multiform.submit(function(event, isValid) {
        showWaitDialog();

        if ($(".block").length == 0) {
            window.location.href = $(".go-back").attr("href");
            event.preventDefault();
            return;
        }

        $(this).find("#form_prefixes").val(formsPrefixes.join(","));
        $(this).find("#delete_ids").val(deleteIds.join(","));

        if ($(this).find("#permissions_form_prefixes").length > 0)
            $(this).find("#permissions_form_prefixes").val(permissionsFormsPrefixes.join(","));

        if (isValid) {
            return;
        }

        event.preventDefault();
        validateApiForm($(this));
    });

    $multiform.on("validation_error", function() {
        hideWaitDialog();
    });

    bindEvents();
})(jQuery);
