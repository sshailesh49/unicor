from json.decoder import JSONDecodeError
from cloudinary.utils import now
from django.shortcuts import render, redirect
from django.utils.regex_helper import flatten_result
from requests.sessions import Request, session
from rest_framework.views import APIView
from django.http import JsonResponse
from bson import ObjectId
import requests
from datetime import datetime
import time
import base64
import cloudinary
import cloudinary.uploader
import cloudinary.api

from unicor.settings import userdb, leddb, IS_AUTH_SERVER, CLOUDINARY_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, BASE_URL


cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)


def response_messages(response_message, response_data):
    final_response_message = {
        "message": response_message,
        "result": response_data
    }
    return final_response_message


def productPage(request):
    if 'email' in request.session:
        return render(request, 'admin/product_category.html')
    else:
        return redirect('signin')


def productAdd(request):
    if 'email' in request.session:

        productName = request.POST.get('productname')
        productName = productName.upper()
        productImage = request.FILES.get('productimage[]')
        CCT = request.POST.get('cct')
        CRI = request.POST.get('cri')
        voltage = request.POST.get('voltage')
        PF = request.POST.get('pf')
        housing = request.POST.get('housing')
        mounting = request.POST.get('mounting')
        aboutProduct = request.POST.get('aboutproduct')

        statusText = request.POST.get('statustext')
        createdBy = request.session['email']
        createdOn = datetime.now().timestamp()

        if statusText == "Active":
            status = True
        else:
            status = False

        if productImage is not None:
            image = cloudinary.uploader.upload(
                productImage, crop="fit", folder="unicor/product/")
            public_id = image["public_id"]
            extension = image["format"]
            img = cloudinary.CloudinaryImage(public_id, format=extension)
            image_url = img.build_url(height=250, width=230, crop="scale")
        else:
            image_url = ""

        jsondata = [{
            'productName': productName,
            'productImage': image_url,
            'CCT': CCT,
            'CRI': CRI,
            'voltage': voltage,
            'PF': PF,
            'housing': housing,
            'mounting': mounting,
            'aboutProduct': aboutProduct,
            'statusText': statusText,
            'status': status,
            'createdBy': createdBy,
            'createdOn': createdOn,
        }]

        json_data = {"data": jsondata}

        get_all_product = requests.post(
            BASE_URL+"ProductAddAPI/", json=json_data, verify=False)
        if get_all_product.status_code == 404:
            msg = get_all_product.json()
            return redirect('product')
        elif get_all_product.status_code == 500:
            return render(request, 'admin/error500.html')
        elif get_all_product.status_code == 200:
            msg = get_all_product.json()
            return redirect('product')
        elif get_all_product.status_code == 401:
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')


class ProductAddAPI(APIView):
    def post(self, request):
        try:
            get_data = request.data
            for i in get_data['data']:
                productdb = userdb.product.find(
                    {'productName': i['productName']})
                if productdb.count() > 0:
                    message = "Product Name Already Exist"
                    return JsonResponse(message, safe=False, status=200)

                else:
                    userdb.product.insert(i)
                    message = "Product Name Added"
                    return JsonResponse(message, safe=False, status=200)
        except Exception as e:
            print("11110", e)
            message = "Internal Server Error {0]".format(e)
            return JsonResponse(message, safe=False, status=500)


class ProductListAPI(APIView):
    def get(self, request):
        try:
            id = request.GET.get('id')
            product = []
            productdb = userdb.product.find({})
            for i in productdb:
                i['id'] = str(i['_id'])
                del i['_id']
                product.append(i)

            return JsonResponse(product, safe=False, status=200)
        except Exception as e:
            message = "Internal Server Error {0]".format(e)
            return JsonResponse(message, safe=False, status=500)


class ProductDeleteAPI(APIView):
    def delete(self, request):
        id = request.GET.get('id')
        print(id)
        userdb.product.delete_one({'_id': ObjectId(id)})
        message = "Record Sucessfull Delete"
        return JsonResponse(message, safe=False, status=200)


def productUpdate(request):
    if 'email' in request.session:
        try:
            id = request.POST.get('id')
            productName = request.POST.get('productname')
            productName = productName.upper()
            productImage = request.FILES.get('productimage[]')
            productImage1 = request.POST.get('productimage1')
            CCT = request.POST.get('cct')
            CRI = request.POST.get('cri')
            voltage = request.POST.get('voltage')
            PF = request.POST.get('pf')
            housing = request.POST.get('housing')
            mounting = request.POST.get('mounting')
            aboutProduct = request.POST.get('aboutproduct')

            statusText = request.POST.get('statustext')

            if statusText == "Active":
                status = True
            else:
                status = False

            if productImage is not None:
                image = cloudinary.uploader.upload(
                    productImage, crop="fit", folder="unicor/product/")
                public_id = image["public_id"]
                extension = image["format"]
                img = cloudinary.CloudinaryImage(public_id, format=extension)
                image_url = img.build_url(height=250, width=230, crop="scale")
                print("1111",image_url)
            else:
                image_url = productImage1
                print( "2222",productImage1)

            jsondata = [{
                'id': id,
                'productName': productName,
                'productImage': image_url,
                'CCT': CCT,
                'CRI': CRI,
                'voltage': voltage,
                'PF': PF,
                'housing': housing,
                'mounting': mounting,
                'aboutProduct': aboutProduct,
                'statusText': statusText,
                'status': status,

            }]

            json_data = {"data": jsondata}
            print( "5555",json_data)

            get_all_product = requests.patch(
                BASE_URL+"ProductUpdateAPI/", json=json_data)
            if get_all_product.status_code == 404:
                #msg = get_all_product.json()
                return redirect('product')
            elif get_all_product.status_code == 500:
                return render(request, 'admin/error500.html')
            elif get_all_product.status_code == 200:
                msg = get_all_product.json()
                return redirect('product')
            elif get_all_product.status_code == 401:
                return redirect('signin')
        except Exception as e:
            print("000000",e)
            message = "Internal Server Error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)

    else:
        del request.session['email']
        return redirect('signin')


class ProductUpdateAPI(APIView):
    def patch(self, request):
        try:
            get_data = request.data
            for i in get_data['data']:
                userdb.product.update({"_id": ObjectId(i['id'])}, {
                    '$set': {
                        'productName': i['productName'],
                        'productImage': i['productImage'],
                        'CCT': i['CCT'],
                        'CRI': i['CRI'],
                        'voltage': i['voltage'],
                        'PF': i['PF'],
                        'housing': i['housing'],
                        'mounting': i['mounting'],
                        'aboutProduct': i['aboutProduct'],
                        


                    }

                })

                message = "Record Sucessfull Update"
                return JsonResponse(message, safe=False, status=200)
        except Exception as e:
            print("11110", e)
            message = "Internal Server Error {0]".format(e)
            return JsonResponse(message, safe=False, status=500)





class ProductDataAPI(APIView):
    def get(self, request):
        try:
            id = request.GET.get('id')
            product = []
            product_data = userdb.product.find({"_id": ObjectId(id)})
            for i in product_data:
                product.append({
                    'id': str(i['_id']),
                    'productName': i['productName'],
                    'productImage': i['productImage'],
                    'CCT': i['CCT'],
                    'CRI': i['CRI'],
                    'voltage': i['voltage'],
                    'PF': i['PF'],
                    'housing': i['housing'],
                    'mounting': i['mounting'],
                    'aboutProduct': i['aboutProduct'],
                })

            return JsonResponse(product, safe=False, status=200)
        except Exception as e:
            message = "Internal Server Error {0]".format(e)
            return JsonResponse(message, safe=False, status=500)
