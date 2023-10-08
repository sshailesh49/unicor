var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {



    mainproductData();





});

function mainproductData() {

    $.ajax({
        url: url_site + 'ProductAppAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {







            var mainproduct = '';

            for (var i = 0; i < data.length; i++) {





                mainproduct = mainproduct + '<div id="1" class="item new col-md-4">\
                <a href="single-product.html">\
                  <div class="featured-item">\
                    <img src=' + data[i].productImage + '  alt="">\
                    <h4>' + data[i].productName + '</h4>\
                 </div>\
                </a>\
              </div>';


















            }


            $("#mainproduct").append(mainproduct)



        },





    });
};