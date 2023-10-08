from json.decoder import JSONDecodeError
from cloudinary.utils import now
from django.shortcuts import render, redirect
from pymongo import message
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


def aboutpage(request):
    if "email" in request.session:
        return render(request, 'admin/about_form.html')
    else:
        return redirect('signin')


def aboutAdd(request):
    if 'email' in request.session:
        aboutTitle = request.POST.get('abouttitle')
        aboutTitle=aboutTitle.upper()
        aboutSubTitle = request.POST.get('aboutsubtitle')
        aboutImage = request.FILES.get('aboutimage[]')
        aboutText1 = request.POST.get('abouttext1')
        aboutText2 = request.POST.get('abouttext2')
        aboutText3 = request.POST.get('abouttext3')
        aboutText4 = request.POST.get('abouttext4')
        statusText = request.POST.get('statustext')
        if aboutImage is not None:
            image = cloudinary.uploader.upload(
                aboutImage, crop="fit", folder="unicor/about/")
            public_id = image['public_id']
            extension = image["format"]
            img = cloudinary.CloudinaryImage(public_id, format=extension)
            image_url = img.build_url(width=570, height=535, crop="scale")
        else:
            image_url = ""

        if "Active" in statusText:
            status = True
        else:
            status = False


        jsondata = [{
            "aboutTitle": aboutTitle,
            "aboutSubTitle": aboutSubTitle,
            "aboutText1": aboutText1,
            "aboutText2": aboutText2,
            "aboutText3": aboutText3,
            "aboutText4": aboutText4,
            "aboutImage": image_url,
            "statusText": statusText,
            "status": status,
            "createdBy": request.session['email'],
            "createdOn":datetime.now().timestamp(),
        }]

        json_data = {'data': jsondata}
     
        print(BASE_URL)

        get_about = requests.post(BASE_URL+'AboutAddAPI/', json=json_data)
      
        if get_about.status_code == 404:
            msg = get_about.json()
            return redirect('about')
        elif get_about.status_code == 200:
            msg = get_about.json()
            return redirect('about')
        elif get_about.status_code == 500:
            msg = get_about.json()
            return render(request, 'admin/error500.html')
        elif get_about.status_code == 401:
            msg = get_about.json()
            return redirect('signin')
    else:
        del request.session["email"]
        return redirect('signin')


class AboutAddAPI(APIView):
    def post(self, request):
        try:
            get_data = request.data
            
            for i in get_data['data']:
              
                aboutdb = userdb.about.find({"aboutTitle": i['aboutTitle']})
                if aboutdb.count() > 0:
                    message = "About Title already exist"
                    return JsonResponse(message, safe=False, staus=404)
                else:
                    userdb.about.insert(i)
                    message = "About Record Sucessfull Added"
                    return JsonResponse(message, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class AboutListAPI(APIView):
    def get(self, request):
        try:
            get_about = userdb.about.find({})
            about = []
            for i in get_about:
                i['id'] = str(i['_id'])
                del i['_id']
                about.append(i)
            print(about)
            return JsonResponse(about, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class AboutDeleteAPI(APIView):
    def delete(self, request):
        id = request.GET.get("id")
        aboutDb = userdb.about.delete_one({"_id": ObjectId(id)})
        message = "Record sucessfully delete"
        return JsonResponse(message, safe=False, status=200)


def aboutUpdate(request):
    if 'email' in request.session:
        id = request.POST.get('id')
       
        aboutTitle = request.POST.get('abouttitle')
        aboutTitle=aboutTitle.upper()
        aboutSubTitle = request.POST.get('aboutsubtitle')
       
        aboutImage = request.FILES.get('aboutimage[]')
        aboutImage1 = request.POST.get('aboutimage1')
        aboutText1 = request.POST.get('abouttext1')
       
        aboutText2 = request.POST.get('abouttext2')
        aboutText3 = request.POST.get('abouttext3')
        aboutText4 = request.POST.get('abouttext4')
        statusText = request.POST.get('statustext')
      
        if aboutImage is not None:
            image = cloudinary.uploader.upload(
                aboutImage, crop="fit", folder="unicor/about/")
            public_id = image['public_id']
            extension = image["format"]
            img = cloudinary.CloudinaryImage(public_id, format=extension)
            image_url = img.build_url(width=570, height=535, crop="scale")
        else:
            image_url = aboutImage1

        if  statusText == "Active":
          
            status = True
        else:
            status = False

        jsondata = [{
            "id":id,
            "aboutTitle": aboutTitle,
            "aboutSubTitle": aboutSubTitle,
            "aboutText1": aboutText1,
            "aboutText2": aboutText2,
            "aboutText3": aboutText3,
            "aboutText4": aboutText4,
            "aboutImage": image_url,
            
            
            "statusText": statusText,
            "status": status,

        }]
       

        json_data = {"data": jsondata}
        print( "agyaaaa",json_data)

        get_about = requests.patch(BASE_URL+"AboutUpdateAPI/", json=json_data,verify=False)
        if get_about.status_code == 404:
            msg = get_about.json()
            return redirect('about')
        elif get_about.status_code == 200:
            msg = get_about.json()
            return redirect('about')
        elif get_about.status_code == 500:
            msg = get_about.json()
            return render(request, 'admin/error500.html')
        elif get_about.status_code == 401:
            msg = get_about.json()
            return redirect('signin')
    else:
        del request.session["email"]
        return redirect('signin')


class AboutUpdateAPI(APIView):
    def patch(self, request):
        try:
            get_data = request.data
            for i in get_data['data']:
                print("arshi",i)
               
                userdb.about.update({"_id": ObjectId(i['id'])}, {
                    '$set': {
                        "aboutTitle": i['aboutTitle'],
                        "aboutSubTitle": i['aboutSubTitle'],
                        "aboutText1": i['aboutText1'],
                        "aboutText2": i['aboutText2'],
                        "aboutText3": i['aboutText3'],
                        "aboutText4": i['aboutText4'],
                        "aboutImage": i['aboutImage'],
                        "statusText": i['statusText'],

                    }
                })
                message=[{
                'message':'Logo sucessfully update..'
            }]
            print(message)
            sucess_message=response_messages(0,message)
            return JsonResponse(sucess_message,safe=False,status=200)
        except Exception as e:
            print("88888",e)
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class AboutDataAPI(APIView):
    def get(self, request):
        try:
            about = []
            id = request.GET.get('id')
            get_data = userdb.about.find({'_id': ObjectId(id)})
            for i in get_data:
                about.append({
                    'id': str(i['_id']),
                    "aboutTitle": i['aboutTitle'],
                    "aboutSubTitle": i['aboutSubTitle'],
                    "aboutText1": i['aboutText1'],
                    "aboutText2": i['aboutText2'],
                    "aboutText3": i['aboutText3'],
                    "aboutText4": i['aboutText4'],
                    "aboutImage": i['aboutImage'],
                })
            return JsonResponse(about,safe=False,status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            print(message)
            return JsonResponse(message, safe=False, status=500)


