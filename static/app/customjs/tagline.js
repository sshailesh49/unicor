var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {



    tagData();






});

function tagData() {

    $.ajax({
        url: url_site + 'TaglineAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {










            $("#tagtitle").html(data[0].taglineTitle)
            $("#tagtext1").html(data[0].taglineText1)
            $("#tagtext2").html(data[0].taglineText2)









        }







    });

};