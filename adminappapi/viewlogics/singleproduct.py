from logging import exception
from cloudinary.utils import now
from django.shortcuts import render, redirect
from requests.sessions import session
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
# Create your views here.

cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)


def response_messages(response_message, response_data):
    '''

    '''
    final_response_message = {
        "message": response_message,
        "result": response_data
    }
    return final_response_message


def singlePage(request):
    if 'email' in request.session:
        return render(request, 'admin/single_product.html')
    else:
        return redirect('signin')


def singleAdd(request):
    if 'email' in request.session:
        #token = request.session['accessToken']

        #headers = {"Authorization": token}
        productId = request.POST.get('productid')
        wattage = request.POST.get('wattage')
        itemcode = request.POST.get('itemcode')
        lumen = request.POST.get('lumen')
        cutout = request.POST.get('cutout')
        design = request.POST.get('design')
        size = request.POST.get('size')
        statusText = request.POST.get('statustext')

        if  statusText =="Active":
            status = True
        else:
            status = False

        jsondata_submit = [{

            'productId': productId,
            'wattage': wattage,
            'itemcode': itemcode,
            'lumen': lumen,
            'cutout': cutout,
            'design': design,
            'size': size,
            'status': status,
            'statusText': statusText,
            'createdBy': request.session['email'],
            'createdOn':datetime.now().timestamp()
        }]
        json_data = {"data": jsondata_submit}
        print('--',BASE_URL)
        get_all_social = requests.post(
            BASE_URL + "SingleProductAddAPI/", json=json_data)
        if get_all_social.status_code == 404:
            msg = get_all_social.json()
            return redirect('/adminpanel/singleadmin/')
        elif get_all_social.status_code == 500:
            return render(request, 'admin/error500.html')
        elif get_all_social.status_code == 200:
            msg = get_all_social.json()
            return redirect('/adminpanel/singleadmin/')
        elif get_all_social.status_code == 401:
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')


class SingleProductAddAPI(APIView):
    def post(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            get_social = request.data
            for i in get_social['data']:
                userdb.singleproduct.insert(i)
                message = "Social Link SuccessFully Added"

                return JsonResponse(message, safe=False, status=200)
        except:
            message = [
                {
                    "message": "Internal Server Error"
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)


class SingleProductListAPI(APIView):

    def get(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            #id = request.GET.get('id')

            single = []
            get_data = userdb.singleproduct.find({})
            
            for i in get_data:
                    
                
                    name=userdb.product.find({'_id':ObjectId(i['productId'])})
                    print("ttttt",name)
                    for j in name:
                        p=(j["productName"])
                        print(p)
                       
                
                        i['id']= str(i['_id'])
                        i['productId']=p
                    
                        del i['_id']
                        
                        
                    
                        single.append(i)
                        print(single)


                
            return JsonResponse(single, safe=False, status=200)
        except:
            message = [
                {
                    "message": "Internal Server Error"
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)


class SingleProductDataAPI(APIView):
    '''
    
    '''

    def get(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            id = request.GET.get('id')
            single = []
            get_social = userdb.singleproduct.find({"_id": ObjectId(id)})

            for i in get_social:
               # print("23232",i['facebook'])
                single.append({
                    'Id': str(i['_id']),
                    'productId': i['productId'],
                    'itemcode': i['itemcode'],
                    'lumen': i['lumen'],
                    'cutout': i['cutout'],
                     'design': i['design'],
                    'size': i['size'],


                })
            return JsonResponse(single, safe=False, status=200)
        except Exception as e:
            message = [
                {
                    "message": "Internal Server Error{e}".format(0)
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)


class SingleProductDeleteAPI(APIView):

    def delete(self, request):
        # try:
        #token = request.META['HTTP_AUTHORIZATION']
        id = request.GET.get('id')

        userdb.singleproduct.delete_one({'_id': ObjectId(id)})
        message = [
            {
                "message": "record SuccessFully Removed"
            }
        ]
        return JsonResponse(message, safe=False, status=200)
    

def singleUpdate(request):
    if 'email' in request.session:
        #token = request.session['accessToken']

        #headers = {"Authorization": token}
        id=request.POST.get('id')
        productId = request.POST.get('productid')
        wattage = request.POST.get('wattage')
        itemcode = request.POST.get('itemcode')
        lumen = request.POST.get('lumen')
        cutout = request.POST.get('cutout')
        design = request.POST.get('design')
        size = request.POST.get('size')
        statusText = request.POST.get('statustext')

        if  statusText =="Active":
            status = True
        else:
            status = False

        jsondata_submit = [{
            
             'id':id,
            'productId': productId,
            'wattage': wattage,
            'itemcode': itemcode,
            'lumen': lumen,
            'cutout': cutout,
            'design': design,
            'size': size,
            'status': status,
            'statusText': statusText,
           
        }]
        json_data = {"data": jsondata_submit}
        print(json_data,'-----',BASE_URL)
        get_all_single = requests.patch(
            BASE_URL + "SingleProductUpdateAPI/", json=json_data)
        print(get_all_single.status_code)
        if get_all_single.status_code == 404:
            msg = get_all_single.json()
            return redirect('/adminpanel/singleadmin/')
        elif get_all_single.status_code == 500:
            return render(request, 'admin/error500.html')
        elif get_all_single.status_code == 200:
            msg = get_all_single.json()
            return redirect('/adminpanel/singleadmin/')
        elif get_all_single.status_code == 401:
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')


class SingleProductUpdateAPI(APIView):
    def patch(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']
            print("1234")
            get_single = request.data
            print(get_single)
            for i in get_single['data']:
                userdb.singleproduct.update({'_id':ObjectId(i['id'])},
                                            {
                    '$set':{
                        'productId':i['productId'],
                        'wattage':i['wattage'],
                        'itemcode':i['itemcode'],
                        'lumen':i['lumen'],
                        'cutout':i['cutout'],
                        'design':i['design'],
                        'size':i['size'],
                        'statusText':i['statusText'],
                        
                        
                    }
                })
                print(i)
            message = "Record  SuccessFully Updated"

            return JsonResponse(message, safe=False, status=200)
        except Exception as e:
            print('-----',e)
            message = [
                {
                    "message": "Internal Server Error"
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)