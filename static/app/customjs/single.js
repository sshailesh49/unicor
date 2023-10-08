var url_site = 'http://127.0.0.1:8000/'

$(document).ready(function() {


    singleData();




});



function singleData() {


    $.ajax({
        url: url_site + 'ProductAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',

        success: function(data, textStatus, xhr) {






            for (var i = 0; i < data.length; i++) {

                $("a#facebook").attr('href', data[i].facebook)
                $("a#instagram").attr('href', data[i].instagram)
                $("a#twitter").attr('href', data[i].twitter)
                $("a#youtube").attr('href', data[i].youtube)

            }






        },





    });
};