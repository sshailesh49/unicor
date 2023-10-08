var url_site = 'http://127.0.0.1:8000/'


var readUrl = function(file) {
    var input = file.target;

    var reader = new FileReader();
    reader.onload = function() {
        var dataURL = reader.result;
        var output = document.getElementById('output');
        output.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
};


$(document).ready(function() {


    FillData1()


});

function FillData1() {

    $.ajax({
        url: url_site + 'adminpanel/AboutListAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {



            var table;
            table = $('#datatable').DataTable();
            table.clear()
            var trHTML = '';

            for (var i = 0; i < data.length; i++) {
                trHTML = [`<div style="text-align: center;">${(i + 1)}</div>`,

                    `<div style="text-align: center;">${data[i].aboutTitle}</div>`,
                    `<div style="text-align: center;">${data[i].aboutSubTitle}</div>`,
                    `<div style="text-align: center;">${data[i].aboutText1}</div>`,
                    `<div style="text-align: center;">${data[i].aboutText2}</div>`,
                    `<div style="text-align: center;">${data[i].aboutText3}</div>`,
                    `<div style="text-align: center;">${data[i].aboutText4}</div>`,
                    `<div style="text-align: center;"><img src="${data[i].aboutImage}" width="100" height=50></div>`,
                    `<div style="text-align: center;">${data[i].statusText}</div>`,
                    `<div style="text-align: center;">${data[i].createdBy}</div>`,
                    `&nbsp;&nbsp;<a  data-toggle="modal" data-target="#user"  onclick=UpdateBtn("${data[i].id}") style="color:blue"><i class="fa fa-pencil-square-o" style="font-size:20px;"></i></a>&nbsp;&nbsp;<a onclick=DeleteBtn("${data[i].id}") style="color:red"><i class="fa fa-trash" style="font-size:20px;"></i></a></div>`
                ]
                table.row.add(trHTML);

            }

            table.draw();


        },





    });
};




function DeleteBtn(id)

{


    swal({
            title: "Are you sure to delete ?",
            text: "You will not be able to recover this file !!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, delete it !!",
            cancelButtonText: "No, cancel it !!",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function(isConfirm) {
            if (isConfirm) {
                var my_data = {
                    "data": [{
                        "id": id
                    }]
                }

                $.ajax({
                    url: url_site + 'adminpanel/AboutDeleteAPI/?id=' + id,
                    type: 'delete',
                    //headers: {"Authorization": AUTH_TOKEN},
                    dataType: '',
                    contentType: 'application/json',
                    data: JSON.stringify(my_data),
                    success: function(data, textStatus, xhr) {

                        location.reload()
                    },
                    error: function(request, status, error) {
                        console.log(request.status);
                        if (request.status == 401) {
                            window.location.replace(url_admin + "signin/");
                        }
                    }

                });

            } else {
                swal("Cancelled !!", "Hey, your imaginary file is safe !!", "error");
            }

        });


};






function UpdateBtn(id) {




    $.ajax({
        url: url_site + 'adminpanel/AboutDataAPI/?id=' + id,
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',

        success: function(data, textStatus, xhr) {

            for (var i = 0; i < data.length; i++) {
                $("#userprof").html('');
                $("#userprof").append(
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">About Title</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].aboutTitle + '" name="abouttitle"   />' +
                    '<input class="form-control" type="hidden" value="' + id + '" name="id" >' +
                    '</div>' +
                    '</div>'

                    +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">About Sub Title</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].aboutSubTitle + '" name="aboutsubtitle"   />' +
                    '</div>' +
                    '</div>'

                    +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Text1</label>' +
                    '<div class="col-sm-6">' +
                    '<textarea id="abouttext3" rows="5" cols="400"  value="' + data[i].aboutText1 + '"  name="abouttext1">' +
                    '</textarea>' +
                    '</div>' +
                    '</div>' +


                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Text2</label>' +
                    '<div class="col-sm-6">' +
                    '<textarea id="abouttext3" rows="5" cols="400"  value="' + data[i].aboutText2 + '"  name="abouttext2">' +
                    '</textarea>' +
                    '</div>' +
                    '</div>' +

                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Text3</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].aboutText3 + '" name="abouttext3"   />' +
                    '</div>' +
                    '</div>' +

                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Text4</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].aboutText4 + '" name="abouttext4"   />' +
                    '</div>' +
                    '</div>' +






                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">aboutImage</label>' +
                    '<div class="col-sm-6">' +
                    '<input type="file" id="slider-upload" name="aboutimage[]" onchange="readUrl(event)" class="form-control" accept="image/*">'

                    +

                    '<input type="hidden"  class="form-control"  value="' + data[i].aboutImage + '" name="aboutimage1"   />' +
                    '</div>' +
                    '</div>'


                    +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">statusText</label>' +
                    '<div class="col-sm-6">' +
                    '<select class="form-control" name="statustext">' +
                    '<option value="Active">Active</option>' +
                    '<option value="Inactive">Inactive</option>' +
                    '</select>'

                    +
                    '</div>' +
                    '</div>'


                    +
                    '</div>' +
                    '</div>');
                $('#blah').hide();
                $('#blah1').hide();


            }


        },
        error: function(request, status, error) {
            console.log(request.status);
            if (request.status == 401) {
                window.location.replace(url_admin + "signin/");

            }
        }
    });


}