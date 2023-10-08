var url_site = 'http://127.0.0.1:8000/'
$(document).ready(function() {


    singleData2()


});

function singleData2() {

    $.ajax({
        url: url_site + 'adminpanel/SingleProductListAPI/',
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

                    `<div style="text-align: center;">${data[i].productId}</div>`,
                    `<div style="text-align: center;">${data[i].wattage}</div>`,
                    `<div style="text-align: center;">${data[i].itemcode}</div>`,
                    `<div style="text-align: center;">${data[i].lumen}</div>`,
                    `<div style="text-align: center;">${data[i].cutout}</div>`,
                    `<div style="text-align: center;">${data[i].design}</div>`,
                    `<div style="text-align: center;">${data[i].size}</div>`,
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
                    url: url_site + 'adminpanel/SingleProductDeleteAPI/?id=' + id,
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
        url: url_site + 'adminpanel/SingleProductDataAPI/?id=' + id,
        type: 'get',
        //headers: {"Authorization": AUTH_TOKEN},
        dataType: 'json',
        success: function(data, textStatus, xhr) {


            for (var i = 0; i < data.length; i++) {
                $("#userprof").html('');
                $("#userprof").append(
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Product Name</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].productId + '" name="productid"   />' +
                    '<input class="form-control" type="hidden" value="' + id + '" name="id" >' +
                    '</div>' +
                    '</div>' +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Wattage</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].wattage + '" name="wattage"   />' +
                    '</div>' +
                    '</div>' +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Item Code</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].itemcode + '" name="itemcode"   />' +
                    '</div>' +
                    '</div>' +

                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Lumen</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].lumen + '" name="lumen"   />' +
                    '</div>' +
                    '</div>' +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Cutout(mm)</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].cutout + '" name="cutout" />' +
                    '</div>' +
                    '</div>' +

                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Design</label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].design + '" name="design"  />' +
                    '</div>' +
                    '</div>' +
                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">Size </label>' +
                    '<div class="col-sm-6">' +
                    '<input class="form-control"  value="' + data[i].size + '" name="size"   />' +
                    '</div>' +
                    '</div>' +





                    '<div class="form-group row">' +
                    '<label for="oldpass" class="col-sm-4 control-label">statusText</label>' +
                    '<div class="col-sm-6">' +
                    '<select class="form-control" name="statustext">' +
                    '<option value="Inactive">Inactive</option>' +
                    '<option value="Active">Active</option>' +

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