$(document).ready(function () {
    // Modal Slide
    $('#subscribeLink').click(function() { 
       $('#loginModal').modal("hide"); 
    });

    $('#mapid').css('display', 'none');
    
    // Alert hide after 3s
    setTimeout(function(){$(".alert").fadeOut('normal');}, 3000);

    //Search users
    var markerList = new Array();
    $('.searchForm').on('submit', function(event){
        event.preventDefault();
        console.log($('#searchInput').val()) // check value
        var searchInterest = $('#searchInput').val();
        $.ajax({
            type: "GET",
            url: "search/",
            data: {'searchInterest': searchInterest},
            dataType: "json",
            success: function (data) {
                if (data) {
                    if (data.noResult) {
                        console.log('No result');
                        $('#mapid').css('display', 'none');
                        $('#noResult').html('<p>Aucun résultat :(</p>');
                    }
                    else {
                        $('#noResult').empty();
                        $('#mapid').css('display', 'block');
                        //Markers

                        //Delete old markers
                        if (markerList != undefined) {
                            $.each(markerList, function (index, value) { 
                                mymap.removeLayer(value);
                                markerList = new Array();
                            });
                        }

                        //Set new markers
                        $.each(data, function (index, value) { 
                            var marker = L.marker([value.Lng, value.Lat]).addTo(mymap);
                            marker.bindPopup("<b>" + value.name + "</b>").openPopup();
                            markerList.push(marker);
                            mymap.addLayer(marker);
                            console.log(markerList);
                        });
                    }
                }
            }
        });
    });
});