var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {



    aboutData();






});

function aboutData() {

    $.ajax({
        url: url_site + 'AboutAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {
            console.log(data)







            for (var i = 0; i < data.length; i++) {

                $("#head").html(data[i].aboutTitle)
                $("#subhead").html(data[i].aboutSubTitle)
                $("#text1").html(data[i].aboutText1)
                $("#text2").html(data[i].aboutText2)
                $("#text3").html(data[i].aboutText3)
                $("#text4").html(data[i].aboutText4)
                $("img#aboutimage").attr('src', data[i].aboutImage)


            }







        },





    });
};