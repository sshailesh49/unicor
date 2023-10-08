var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {



    banner();







});

function banner() {

    $.ajax({
        url: url_site + 'BannerAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {







            for (var i = 0; i < data.length; i++) {


                var imageUrl = data[i].sliderImage;
                $(".banner").css("background-image", "url(" + imageUrl + ")");
                $("#bannertitle").html(data[i].sliderTitle)


            }







        },





    });
};