$(document).ready(function () {   
    $("#cityInput").autocomplete({
        source : "complete-city/",
        minLength : 1,    
    });
});

