$(document).ready(function () {
    // Modal Slide
    $('#subscribeLink').click(function () {
        $('#loginModal').modal("hide");
    });
    
    // hide the map on ready load page
    $('#mapid').css('display', 'none');
    
    // Alert hide after 3s
    setTimeout(function () { $(".alert").fadeOut('normal'); }, 3000);
    
    if (cookies == true){
        window.setTimeout(function () {$('#cookiesModal').modal("show"); }, 3000 );
    };
    
    $('#cookiesButton').click(function () { 
        $.ajax({
            type: "GET",
            url: "acceptCookies/",
            data: {"setCookieAccept": 'Horray !'},
            dataType: "json"
        });
        
    });
    
});