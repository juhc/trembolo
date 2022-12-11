$(document).ready(function () {
    $("#address").suggestions({
        token: "769af09233b6a876d49ff4d46a81778823647a36",
        type: "ADDRESS",
        /* Вызывается, когда пользователь выбирает одну из подсказок */
        onSelect: function (suggestion) {
            console.log(suggestion);
        }
    });
});