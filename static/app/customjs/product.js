var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {



    myproductData();





});

function myproductData() {

    $.ajax({
        url: url_site + 'ProductAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {







            for (var i = 0; i < data.length; i++) {






                $("img#owlimage").attr('src', data[2].productImage)
                $("#owlmame").html(data[2].productName)















            }






        },





    });
};