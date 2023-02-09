document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        $(".alert").delay(1000).slideUp(200, function () {
            $(this).alert('close');
        });
    }, 3000);
});
