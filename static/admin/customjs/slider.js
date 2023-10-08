var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {


    FillData1()


});

function FillData1() {

    $.ajax({
        url: url_site + 'adminpanel/SliderListAPI/',
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

                    `<div style="text-align: center;">${data[i].sliderName}</div>`,
                    `<div style="text-align: center;">${data[i].sliderTitle}</div>`,

                    `<div style="text-align: center;"><img src="${data[i].sliderImage}" width="100" height=50></div>`,
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
                    url: url_site + 'adminpanel/SliderDeleteAPI/?id=' + id,
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
        url: url_site + 'adminpanel/SliderDataAPI/?id=' + id,
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {


            for (var i = 0; i < data.length; i++) {
                $("#userprof").html('');
                $("#userprof").append(
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">sliderName</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].sliderName + '" name="slidername"  required="required" />' +
                    '<input class="form-control" type="hidden" value="' + id + '" name="id" >' +
                    '</div>' +
                    '</div>' +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">sliderTitle</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].sliderTitle + '" name="slidertitle"   />' +

                    '</div>' +
                    '</div>'

                    +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">sliderImage</label>' +
                    '<div class="col-sm-6">' +
                    '<input type="file" id="slider-upload"  class="form-control"   name="sliderImage[]"  onchange="readUrl(event)" accept="image/*" />' +
                    '<img id="output" style="height:100px;width:100px;" alt=""/>' +
                    '<input type="hidden" class="form-control"  value="' + data[i].sliderImage + '" name="sliderimage1"   />' +
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