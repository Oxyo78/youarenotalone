$(document).ready(function () {
    var liste = [
        "abc hola !",
        "acb",
        "def"
    ];
    
    $("#cityInput").autocomplete({
        source : "complete-city/",
        minLength : 1,    
    });
});

