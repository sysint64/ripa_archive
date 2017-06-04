$(document).ready(function() {
    $(".data-link").click(function() {
        location.href = $(this).data("href");
    });
});
