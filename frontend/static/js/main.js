$.fn.exist = function (elem) {
    return elem.length > 0;
};

$(document).ready(function() {
    $(".data-link").click(function() {
        location.href = $(this).data("href");
    });

    $(".data-double-click-link").dblclick(function() {
        location.href = $(this).data("href");
    });
});
