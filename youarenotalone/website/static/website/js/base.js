$(document).ready(function () {
    // Modal Slide
    $('#subscribeLink').click(function() { 
       $('#loginModal').modal("hide"); 
    });
    
    // Alert hide after 3s
    setTimeout(function(){$(".alert").fadeOut('normal');}, 3000);
});
