$(document).ready(function () {
    // Modal Slide
    $('#subscribeLink').click(function () {
        $('#loginModal').modal("hide");
    });

    // hide the map on ready load page
    $('#mapid').css('display', 'none');

    // Alert hide after 3s
    setTimeout(function () { $(".alert").fadeOut('normal'); }, 3000);

});
