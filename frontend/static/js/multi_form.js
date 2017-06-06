(function ($) {
    $("input").addClass("form-control");
    const $blockPrimary = $("#block-primary");
    const primaryBlockHtml = $blockPrimary.html();
    const formPrefix = "block";
    var lastBlockNumber = 0;
    var forms = [];

    $blockPrimary.find(".remove-block").remove();

    function bindEvents() {
        $(".block").click(function() {
            $(".multi-form").find(".block").removeClass("active");
            $(this).addClass("active");
        });

        $(".remove-block").click(function() {
            const $block = $(this).closest(".block");
            const index = forms.indexOf($block.data("prefix"));
            forms.splice(index, 1);
            console.log(forms);
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
        $block.find("input").attr("name", function(index, attr) { return prefix + "-" + attr; });
        $("#block-cursor").before($block);

        forms.push(prefix);
        console.log(forms);
    }

    $(".add-block-button").click(function() {
        putBlock();
        rebindEvents();
    });

    $("#multiform").submit(function(e) {
        e.preventDefault();
        $(this).find("input[name=forms]").val(forms.join(","));
    });

    bindEvents();
})(jQuery);
