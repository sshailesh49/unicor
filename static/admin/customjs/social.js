var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {


    FillData1()



});

function FillData1() {

    $.ajax({
        url: url_site + 'adminpanel/SocialListAPI/',
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {
            alert(textStatus.length)


            var table;
            table = $('#datatable').DataTable();
            table.clear()
            var trHTML = '';

            for (var i = 0; i < data.length; i++) {
                trHTML = [`<div style="text-align: center;">${(i + 1)}</div>`,

                    `<div style="text-align: center;">${data[i].facebook}</div>`,
                    `<div style="text-align: center;">${data[i].instagram}</div>`,
                    `<div style="text-align: center;">${data[i].twitter}</div>`,
                    `<div style="text-align: center;">${data[i].youtube}</div>`,
                    `<div style="text-align: center;">${data[i].status}</div>`,

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
                    url: url_site + 'adminpanel/SocialDeleteAPI/?id=' + id,
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


    id = id
    $.ajax({
        url: url_site + 'adminpanel/SocialDataAPI/?id=' + id,
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {


            for (var i = 0; i < data.length; i++) {
                $("#userprof").html('');
                $("#userprof").append(
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Faceboo</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].facebook + '" name="facebook"  />' +
                    '<input class="form-control" type="hidden" value="' + id + '" name="id" >' +
                    '</div>' +
                    '</div>'

                    +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Instagram</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].instagram + '" name="instagram"   />' +
                    '</div>' +
                    '</div>'

                    +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Twitter</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].twitter + '" name="twitter"   />' +
                    '</div>' +
                    '</div>' +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Youtube</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].youtube + '" name="youtube"  />' +
                    '</div>' +
                    '</div>'







                    +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">statusText</label>' +
                    '<div class="col-sm-6">' +
                    '<select class="form-control" name="statusText">' +
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