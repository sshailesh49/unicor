import json
from json.decoder import JSONDecodeError
from cloudinary.utils import now
from django.shortcuts import render,redirect
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

from unicor.settings import userdb,leddb,IS_AUTH_SERVER,CLOUDINARY_NAME,CLOUDINARY_API_KEY,CLOUDINARY_API_SECRET,BASE_URL


cloudinary.config(
    cloud_name =CLOUDINARY_NAME,
    api_key =CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET
)


def response_messages(response_message,response_data):
    final_response_message ={
        "message":response_message,
        "result":response_data
    }
    return final_response_message

def logopage(request):
    if "email" in request.session:
         return render(request,'admin/logo_form.html')
    else:
        return redirect('signin')
    

def logoAdd(request):
    if "email" in request.session:
        logoName = request.POST.get('logoname')
        logoImage =request.FILES.get('logoimage[]')
        statusText =request.POST.get("statustext")
        
        if logoImage  is not None:
            image=cloudinary.uploader.upload(logoImage,crop="fit",folder="unicor/logo/")
            public_id = image['public_id']
            extension = image["format"]
            img = cloudinary.CloudinaryImage(public_id,format=extension)
            image_url = img.build_url(width=180,height=75, crop="scale")
        else:
            image_url=""   
        
        if "Active" in statusText:
            status=True
        else:
            status=False
        
        jsondata= [{
            "logoName":logoName,
            "logoImage":image_url,
            "statusText":statusText,
            "status":status,
            "createdBy":request.session["email"],
            "createdOn":datetime.now().timestamp()
            }]
        
        json_data={"data":jsondata}
        
        get_logo = requests.post(BASE_URL+"LogoAddAPI/",json=json_data)
        
        if get_logo.status_code == 404:
            msg= get_logo.json()
            return redirect('logo')
        elif get_logo.status_code == 500:
            msg=get_logo.json()
            return render(request,'admin/error500.html')
        elif get_logo.status_code == 200:
            msg=get_logo.json()
            return redirect("logo")
        elif get_logo.status_code==401:
            msg = get_logo.json()
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')
    
    
class LogoAddAPI(APIView):
    
      def post(self,request):
          #if "email" in request.session:
              try:
                  get_logo=request.data
                  for i in get_logo["data"]:
                  
                    logodb=userdb.logo.find({"logoName":i["logoName"]})
                    print(logodb.count())
                    if logodb.count()>0:
                        
                        message ="Logo Name Already exist"
                        return JsonResponse(message,safe=False,status=404)
                    else:
                        userdb.logo.insert(i)
                        message="Logo Sucessfull Added"
                        return JsonResponse(message,safe=False,status=200)
              except Exception as e:
                  message = "Internal server error {0}" .format(e) 
                  
                  return JsonResponse(message,safe=False,status=500) 
         # else:
             # message ="Please login  again"
              #return JsonResponse(message,safe=False,status=401)
              
    
    
class LogoListAPI(APIView):
    def get(self, request):
        try:
            logo = []
            get_logo = userdb.logo.find({})

            for i in get_logo:
                i['id'] = str(i['_id'])

                del i['_id']
                logo.append(i)

            return JsonResponse(logo, safe=False, status=200)
        except Exception as e:
            message = "internal server error"
            return JsonResponse(message, safe=False, status=500)
        
class LogoDataAPI(APIView):
    def get(self,request):
        try:
            logo=[]
            id=request.GET.get('id')
            logo_data=userdb.logo.find({'_id':ObjectId(id)})
            for i in logo_data:
                logo.append({
                    'id': str(i['_id']),
                    'logoName':i['logoName'],
                    'logoImage':i['logoImage']
                })
            return JsonResponse(logo,safe=False,status=200)
        except Exception as e:
            message = [{
                "message": "internal server Error!!!{0}".format(e)
            }]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)
                
            


class LogoDeleteAPI(APIView):
    def delete(self,request):
        id=request.GET.get("id")
        userdb.logo.delete_one({"_id":ObjectId(id)})
        message="data sucessfully delete"
        return JsonResponse(message,safe=False,status=200)
              
def logoUpdate(request):
    if 'email' in request.session:
        id=request.POST.get('id')
        print("999999999999",id)
        logoName=request.POST.get('logoName')
        logoImage =request.FILES.get('logoImage[]')
        logoImage1 = request.POST.get('logoImage1')
        statusText=request.POST.get('statusText')
        if "Active " in statusText:
            status=True
        else:
            status=False
        if logoImage is not None:
            image=cloudinary.uploader.upload(logoImage,crop="fit",folder="unicor/logo/")
            public_id =image['public_id']
            extension = image['format']
            img=cloudinary.CloudinaryImage(public_id,format=extension)
            img_url =img.build_url(width=180,height=75,crop="scale")
       
        else:
            img_url=logoImage1
            
        josondata=[{
            "id":id,
            "logoName":logoName,
            "logoImage":img_url,
            "statusText":statusText,
            "status":status
        }]
        json_data={"data":josondata}
      
        requests.patch(BASE_URL+"LogoUpdateAPI/",json=json_data,verify=False)
     
        return redirect("logo")
    else:
        del request.session["email"]
        return redirect('signin')
    
class LogoUpdateAPI(APIView):
    def patch(self,request):
        print("hello")
        try:
            get_logo = request.data
            
            for i in get_logo['data']:
                print("4444",i)
                
                userdb.logo.update({'_id':ObjectId(i['id'])},{
                  '$set':{
                      'logoName':i['logoName'],
                      'logoImage':i['logoImage'],
                      'statusText':i['statusText']
                                      
                  }  
                })
            message=[{
                'message':'Logo sucessfully update..'
            }]
            print(message)
            sucess_message=response_messages(0,message)
            return JsonResponse(sucess_message,safe=False,status=200)
        except Exception as e:
            print("dgdgdfg",e)
            message=[{
                "message":"internal server error{0}".format(e)
            }]
            error_message=response_messages(2,message)
            return JsonResponse(message,safe=False,status=500)