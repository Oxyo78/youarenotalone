$(document).ready(function () {
    $('.showMessage').click(function () { 
        var idMessage = $(this).attr('value');
        console.log(idMessage);
        $('.messageDetail').load("messages/", "idMessage: idMessage", function () {
            this; // dom element
            
        });
    });
});