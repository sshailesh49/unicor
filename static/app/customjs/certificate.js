var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {



    certi();







});

function certi() {

    $.ajax({
        url: url_site + 'CeriAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {







            for (var i = 0; i < data.length; i++) {

                $("#ceri").html(data[i].ceriName)
                $("#detail").html(data[i].ceriText)
                $("img#certiimage").attr('src', data[i].ceriImage)

            }







        },





    });
};