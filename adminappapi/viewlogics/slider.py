from json.decoder import JSONDecodeError
from cloudinary.utils import now
from django.shortcuts import render, redirect
from requests.sessions import session
from rest_framework.views import APIView
from django.http import JsonResponse
from bson import ObjectId, objectid
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


def indexpage(request, msg=""):
    if "email" in request.session:
        return render(request, 'admin/slider_form.html', {'msg': msg})

    else:
        return redirect('signin')


def slideAdd(request):
    if request.session['email']:
        sliderName = request.POST.get('slidername')
        sliderTitle = request.POST.get('slidertitle')
        sliderTitle = sliderTitle.upper()
        #sliderSubTitle = request.POST.get('slidersubtitle')
        sliderImage = request.FILES.get('sliderimage[]')
        statusText = request.POST.get('statustext')

        if sliderImage is not None:
            image = cloudinary.uploader.upload(
                sliderImage, crop='fit', folder='unicor/slider/')
            public_id = image['public_id']
            extension = image['format']
            img = cloudinary.CloudinaryImage(public_id, format=extension)
            img_url = img.build_url(width=1600, height=550, crop="scale")
            

        else:
            img_url = ''

        if "Active" in statusText:
            status = True

        else:
            status = False

        jsondata_submit = [{"sliderName": sliderName,
                            "sliderTitle": sliderTitle,
                            # "sliderSubTitle": sliderSubTitle,
                            "sliderImage": img_url,
                            "status": status,
                            "statusText": statusText,
                            "createdBy": request.session['email'],
                            "createdOn":datetime.now().timestamp()
                            }]

        json_data = {"data": jsondata_submit}
        get_all_slider = requests.post(
            BASE_URL + "SliderAddAPI/", json=json_data)
        if get_all_slider.status_code == 404:

            msg = get_all_slider.json()
            return redirect('/adminpanel/slider/')

        elif get_all_slider.status_code == 500:
            return render(request, 'admin/error500.html')
        elif get_all_slider.status_code == 200:

            msg = get_all_slider.json()
            return redirect('/adminpanel/slider/')
        elif get_all_slider.status_code == 401:
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')


class SliderAddAPI(APIView):
    def post(self, request):
        try:
            get_slider = request.data
            for i in get_slider['data']:
                sliderDB = userdb.slider.find(
                    {'sliderName': i['sliderName'], "status": True})
                if sliderDB.count() > 0:
                    message = " Banner allredy exists"
                    return JsonResponse(message, safe=False, status=404)

                else:
                    userdb.slider.insert(i)
                    message = "Banner sucessfilly added"
                    return JsonResponse(message, safe=False, status=200)

        except Exception as e:
            message = "Internal Server Errer {0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class SliderListAPI(APIView):
    def get(self, request):
        try:
            slider = []
            get_slider = userdb.slider.find({})

            for i in get_slider:
                i['id'] = str(i['_id'])

                del i['_id']
                slider.append(i)

            return JsonResponse(slider, safe=False, status=200)
        except Exception as e:
            message = "internal server error"
            return JsonResponse(message, safe=False, status=500)
        
class SliderDeleteAPI(APIView):
    def delete(self,request):
        id=request.GET.get('id')
        userdb.slider.delete_one({"_id":ObjectId(id)})
        message="Banner sucessfully delete!!"
        return JsonResponse(message,safe=False,status=200)
    
def sliderUpdate(request):
    if 'email' in request.session:
        id=request.POST.get('id')
        sliderName = request.POST.get('slidername')
        sliderTitle = request.POST.get('slidertitle')
        sliderTitle = sliderTitle.upper()
        #sliderSubTitle = request.POST.get('slidersubtitle')
        sliderImage = request.FILES.get('sliderimage[]')
        sliderImage1 = request.POST.get('sliderimage1')
        statusText = request.POST.get('statustext')
        
        if statusText =="Active":
            status=True
            
        else: 
            status=False
            
        
        if sliderImage is not None:
            image = cloudinary.uploader.upload(
            sliderImage, crop='fit', folder='unicor/slider/')
            public_id = image['public_id']
            extension = image['format']
            img = cloudinary.CloudinaryImage(public_id, format=extension)
            img_url = img.build_url(width=1600, height=550, crop="scale")
            

        else:
            img_url = sliderImage1

     

        jsondata_submit = [{'id':id,
                            "sliderName": sliderName,
                            "sliderTitle": sliderTitle,
                            # "sliderSubTitle": sliderSubTitle,
                            "sliderImage": img_url,
                            "status": status,
                            "statusText": statusText,
                            
                            }]

        json_data = {"data": jsondata_submit}
        print(json_data)
        get_all_slider = requests.patch(
            BASE_URL+"SliderUpdateAPI/", json=json_data)
        print(get_all_slider)
        if get_all_slider.status_code == 404:

            msg = get_all_slider.json()
            return redirect('/adminpanel/slider/')

        elif get_all_slider.status_code == 500:
            return render(request, 'admin/error500.html')
        elif get_all_slider.status_code == 200:

            msg = get_all_slider.json()
            return redirect('/adminpanel/slider/')
        elif get_all_slider.status_code == 401:
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')


class SliderUpdateAPI(APIView):
    def patch(self, request):
        
        try:
            get_slider = request.data
            for i in get_slider['data']:
                
                    userdb.slider.update( {'_id':ObjectId(i['id'])},{
                        '$set':{
                            "sliderName":i["sliderName"],
                            
                            "sliderTitle": i['sliderTitle'],
                            # "sliderSubTitle": sliderSubTitle,
                            "sliderImage": i['sliderImage'],
                            "status": i['status'],
                            "statusText":i['statusText'],
                            
                            
                            
                        }
                    })
                    message = "Banner sucessfilly updated"
                    return JsonResponse(message, safe=False, status=200)

        except Exception as e:
            message = "Internal Server Errer {0}".format(e)
            return JsonResponse(message, safe=False, status=500)

class SliderDataAPI(APIView):
    def get(self, request):
        try:
            slider = []
            id=request.GET.get('id')
            
            get_slider = userdb.slider.find({'_id':ObjectId(id)})
         

            for i in get_slider:
                
                slider.append({
                   'id':str(i['_id']),
                   'sliderName':i['sliderName'],
                   'sliderImage':i['sliderImage'],
                   'sliderTitle':i['sliderTitle'],
               
               
                
               })
               

            return JsonResponse(slider, safe=False, status=200)
        except Exception as e:
            message = "internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)
        