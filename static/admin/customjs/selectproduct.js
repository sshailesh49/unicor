var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {


    selectproduct();





});

function selectproduct() {

    $.ajax({
        url: url_site + 'ProductAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {
            console.log(data)

            for (var i = 0; i < data.length; i++) {

                var option = $('<option></option>');
                option.attr('value', data[i].id);
                option.text(data[i].productName);
                $('#myselect').append(option);
            }

        }


    });
};