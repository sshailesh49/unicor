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


def taglinePage(request):
    if "email" in request.session:
        return render(request, 'admin/tagline.html')
    else:
        return redirect('signin')


def taglineAdd(request):
    if 'email' in request.session:
        taglineTitle = request.POST.get('taglinetitle')
        taglineTitle = taglineTitle.upper()
        taglineText1 = request.POST.get('taglinetext1')
        taglineText2 = request.POST.get('taglinetext2')
        statusText = request.POST.get('statustext')
       

        if "Active" in statusText:
            status = True
        else:
            status = False

        

        jsondata = [{
            "taglineTitle": taglineTitle,
            
            "taglineText1": taglineText1,
            "taglineText2": taglineText2,
            
            
            "statusText": statusText,
            "status": status,
            "createdBy": request.session['email'],
            "createdOn":datetime.now().timestamp(),
        }]

        json_data = {'data': jsondata}
        print("qqqq", json_data)
        print(BASE_URL)

        get_tag = requests.post(BASE_URL+'TaglineAddAPI/', json=json_data)
      
        if get_tag.status_code == 404:
            msg = get_tag.json()
            return redirect('tag')
        elif get_tag.status_code == 200:
            msg = get_tag.json()
            return redirect('tag')
        elif get_tag.status_code == 500:
            msg = get_tag.json()
            return render(request, 'admin/error500.html')
        elif get_tag.status_code == 401:
            msg = get_tag.json()
            return redirect('signin')
    else:
        del request.session["email"]
        return redirect('signin')


class TaglineAddAPI(APIView):
    def post(self, request):
        try:
            get_data = request.data
            
            for i in get_data['data']:
               
                aboutdb = userdb.tagline.find({"taglineTitle": i['taglineTitle']})
                if aboutdb.count() > 0:
                    message = "Tagline Title already exist"
                    return JsonResponse(message, safe=False, staus=404)
                else:
                    userdb.tagline.insert(i)
                    message = " Record Sucessfull Added"
                    return JsonResponse(message, safe=False, status=200)
        except Exception as e:
            print(e)
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class TaglineListAPI(APIView):
    def get(self, request):
        try: 
            get_tag = userdb.tagline.find({})
            tagline = []
            for i in get_tag:
                i['id'] = str(i['_id'])
                del i['_id']
                tagline.append(i)
            print(tagline)
            return JsonResponse(tagline, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class TaglineDeleteAPI(APIView):
    def delete(self, request):
        id = request.GET.get("id")
        aboutDb = userdb.tagline.delete_one({"_id": ObjectId(id)})
        message = "Record sucessfully delete"
        return JsonResponse(message, safe=False, status=200)


def taglineUpdate(request):
    if 'email' in request.session:
        id = request.POST.get('id')
        
        taglineTitle = request.POST.get('taglinetitle')
        taglineTitle = taglineTitle.upper()
       
        taglineText1 = request.POST.get('taglinetext1')
        taglineText2 = request.POST.get('teglinetext2')

        statusText = request.POST.get('statustext')
       
        

        if  statusText == "Active":
            
            status = True
        else:
            status = False

        jsondata = [{
            "id":id,
            "taglineTitle": taglineTitle,
           "taglineText1": taglineText1,
           "taglineText2": taglineText2,
           "statusText": statusText,
            "status": status,

        }]
       

        json_data = {"data": jsondata}
        print( "agyaaaa",json_data)

        get_data = requests.patch(BASE_URL+"TaglineUpdateAPI/", json=json_data,verify=False)
        if get_data.status_code == 404:
            msg = get_data.json()
            return redirect('about')
        elif get_data.status_code == 200:
            msg = get_data.json()
            return redirect('about')
        elif get_data.status_code == 500:
            msg = get_data.json()
            return render(request, 'admin/error500.html')
        elif get_data.status_code == 401:
            msg = get_data.json()
            return redirect('signin')
    else:
        del request.session["email"]
        return redirect('signin')


class TaglineUpdateAPI(APIView):
    def patch(self, request):
        try:
            get_data = request.data
            for i in get_data['data']:
               
               
                userdb.tagline.update({"_id": ObjectId(i['id'])}, {
                    '$set': {
                        "taglineTitle": i['taglineTitle'],
                       
                        "taglineText1": i['taglineText1'],
                        "taglineText2": i['taglineText2'], 
                        
                        "statusText": i['statusText'],

                    }
                })
                message=[{
                'message':'Tagline sucessfully update..'
            }]
       
            sucess_message=response_messages(0,message)
            return JsonResponse(sucess_message,safe=False,status=200)
        except Exception as e:
            print("88888",e)
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class TaglineDataAPI(APIView):
    def get(self, request):
        try:
            tagline = []
            id = request.GET.get('id')
            get_data = userdb.tagline.find({'_id': ObjectId(id)})
            for i in get_data:
                tagline.append({
                    'id': str(i['_id']),
                    "taglineTitle": i['taglineTitle'],
                   
                    "taglineText1": i['taglineText1'],
                    "taglineText2": i['taglineText2'],
                  
                })
            return JsonResponse(tagline,safe=False,status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            print(message)
            return JsonResponse(message, safe=False, status=500)


