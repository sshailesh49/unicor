var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {




    contactData1();






});

function contactData1() {

    $.ajax({
        url: url_site + 'ContactAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {

            for (var i = 0; i < data.length; i++) {

                $("#tele").html(data[i].telephone)
                $("#email").html(data[i].email)
                $("#add1").html(data[i].address1)
                $("#add2").html(data[i].address2)
            }

        }


    });
};