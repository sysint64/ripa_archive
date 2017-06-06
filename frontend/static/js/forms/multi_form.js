(function ($) {
    $("input").addClass("form-control");
    const $blockPrimary = $("#block-primary");
    const primaryBlockHtml = $blockPrimary.html();
    const formPrefix = "block";
    var lastBlockNumber = 0;
    var formsPrefixes = [];

    $blockPrimary.find(".remove-block").remove();

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
    }

    function unbindEvents() {
        $(".block").unbind("click");
        $(".remove-block").unbind("click");
    }

    function rebindEvents() {
        unbindEvents();
        bindEvents();
    }

    function putBlock() {
        lastBlockNumber += 1;
        const prefix = formPrefix + parseInt(lastBlockNumber);

        var $block = $("<div/>", {"class": "block", "html": primaryBlockHtml, "data-prefix": prefix});
        const addPrefix = function(index, attr) { return prefix + "-" + attr; };
        $block.find("label").attr("for", addPrefix);
        $block.find("input").attr("name", addPrefix).attr("id", addPrefix);
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
        $(this).find("input[name=forms_prefixes]").val(formsPrefixes.join(","));

        if (isValid)
            return;

        event.preventDefault();
        validateApiForm($(this));
    });

    bindEvents();
})(jQuery);
