var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {




    maincontactData1();






});

function maincontactData1() {

    $.ajax({
        url: url_site + 'ContactAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {

            for (var i = 0; i < data.length; i++) {

                $("#cal").html(data[i].telephone)
                $("#mail").html(data[i].email)
                $("#ad1").html(data[i].address1)
                $("#ad2").html(data[i].address2)
            }

        }


    });
};