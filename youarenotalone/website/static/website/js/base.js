$(document).ready(function () {
    // Modal Slide
    $('#subscribeLink').click(function () {
        $('#loginModal').modal("hide");
    });

    // hide the map on ready load page
    $('#mapid').css('display', 'none');

    // Alert hide after 3s
    setTimeout(function () { $(".alert").fadeOut('normal'); }, 3000);

    //Search users
    var markerList = new Array();
    var markersLayer = L.featureGroup().addTo(mymap);
    $('.searchForm').on('submit', function (event) {
        event.preventDefault();
        console.log($('#searchInput').val()) // check value
        var searchInterest = $('#searchInput').val();
        $.ajax({
            type: "GET",
            url: "search/",
            data: { 'searchInterest': searchInterest },
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
                        // Add scrolling to map
                        // var target = $( "#mapid" );
                        // target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                        // $('#mapid').animate({
                        //     scrollTop: (target.offset().top - 56)
                        //   }, 1000, "easeInOutExpo");

                        //Delete old markers
                        if (markerList != undefined) {
                            $.each(markerList, function (index, value) {
                                mymap.removeLayer(value);
                                markerList = new Array();
                            });
                        }

                        //Set new markers
                        $.each(data, function (index, value) {
                            var marker = L.marker([value.Lng, value.Lat], { title: value.name }).addTo(mymap);
                            var nameLink = '<a class="nav-link mapLink" data-toggle="modal" data-target="#composeModal" href="#">Envoyer un message à ' + value.name + '</a>'
                            marker.bindPopup(nameLink);
                            markerList.push(marker);
                            marker.properties = {};
                            marker.properties.name = value.name;
                            marker.properties.lng = value.Lng;
                            marker.properties.lat = value.Lat;
                            marker.addTo(markersLayer);
                            console.log(markerList);
                        });
                        mymap.setView([markerList[0].properties.lng, markerList[0].properties.lat], 5);
                    }
                }
            }
        });
    });

    // Select user on map
    var userToChat;
    markersLayer.on('click', function (e) {
        userToChat = e.layer.properties;
        mymap.setView([userToChat.lng, userToChat.lat], 6);
        console.log(userToChat.name);
    });


    // Send a message to select user
    $(".composeForm").on('submit', function (event) {
        event.preventDefault();
        var token = jQuery("[name=csrfmiddlewaretoken]").val();
        console.log("Send !");
        var subject = $("#subjectMessage").val();
        var body = $("#bodyMessage").val();
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        });
        $.ajax({
            type: "POST",
            url: "newMessage/",
            data: { 'recipient': userToChat.name, 'subject': subject, 'body': body },
            dataType: "json",
            success: function (data) {
                $('#composeModal').modal("hide");
                $('#alertMessage').html('<div class="alert alert-success fixed-top text-center"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Message envoyé</strong></div>');
                setTimeout(function () { $(".alert").fadeOut('normal'); }, 3000);
                console.log(data);
            }
        });
    });
});
