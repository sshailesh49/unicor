from json.decoder import JSONDecodeError
from cloudinary.utils import now
from django.shortcuts import render,redirect
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

def certificatePage(request):
    if "email" in request.session:
       return render(request,'admin/certificate_form.html')
    else:
        return redirect("signin")

def ceriAdd(request):
    if "email" in request.session:
        ceriName = request.POST.get('ceriName')
        ceriName=ceriName.upper()
        ceriImage =request.FILES.get('ceriImage[]')
        ceriText = request.POST.get('ceriText')
        statusText =request.POST.get("statusText")
        
        if ceriImage  is not None:
            image=cloudinary.uploader.upload(ceriImage,crop="fit",folder="unicor/ceri/")
            public_id = image['public_id']
            extension = image["format"]
            img = cloudinary.CloudinaryImage(public_id,format=extension)
            image_url = img.build_url(width=493,height=128, crop="scale")
        else:
            image_url=""   
        
        if  statusText =="Active":
            status=True
        else:
            status=False
        
        jsondata= [{
            "ceriName":ceriName,
            "ceriImage":image_url,
            "ceriText":ceriText,
            "statusText":statusText,
            "status":status,
            "createdBy":request.session["email"],
            "createdOn":datetime.now().timestamp()
            }]
        
        json_data={"data":jsondata}
        
        get_ceri = requests.post(BASE_URL+"CeriAddAPI/",json=json_data)
        
        if get_ceri.status_code == 404:
            msg= get_ceri.json()
            return redirect('ceri')
        elif get_ceri.status_code == 500:
            msg=get_ceri.json()
            return render(request,'admin/error500.html')
        elif get_ceri.status_code == 200:
            msg=get_ceri.json()
            return redirect("ceri")
        elif get_ceri.status_code==401:
            msg = get_ceri.json()
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')
    
    
class CeriAddAPI(APIView):
    
      def post(self,request):
          #if "email" in request.session:
              try:
                  get_ceri=request.data
                  for i in get_ceri["data"]:
                  
                    ceridb=userdb.certificate.find({"ceriName":i["ceriName"]})
                    
                    if ceridb.count()>0:
                        
                        message ="Ceritificate Name Already exist"
                        return JsonResponse(message,safe=False,status=404)
                    else:
                        userdb.certificate.insert(i)
                        message="Certificate Sucessfull Added"
                        return JsonResponse(message,safe=False,status=200)
              except Exception as e:
                  message = "Internal server error {0}" .format(e) 
                  
                  return JsonResponse(message,safe=False,status=500) 
         # else:
             # message ="Please login  again"
              #return JsonResponse(message,safe=False,status=401)
              
    
    
class CeriListAPI(APIView):
    def get(self, request):
        try:
            ceri = []
            get_ceri = userdb.certificate.find({})
           

            for i in get_ceri:
                
            
                i['id'] = str(i['_id'])

                del i['_id']
                ceri.append(i)
                
            

            return JsonResponse(ceri, safe=False, status=200)
        except Exception as e:
            message = "internal server error"
            return JsonResponse(message, safe=False, status=500)
        
class CeriDataAPI(APIView):
    def get(self,request):
        try:
            ceri=[]
            id=request.GET.get('id')
            ceri_data=userdb.certificate.find({'_id':ObjectId(id)})
            for i in ceri_data:
                ceri.append({
                    'id': str(i['_id']),
                    'ceriName':i['ceriName'],
                    'ceriImage':i['ceriImage'],
                    'ceriText':i['ceriText']
                })
            return JsonResponse(ceri,safe=False,status=200)
        except Exception as e:
            message = [{
                "message": "internal server Error!!!{0}".format(e)
            }]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)
                
            


class CeriDeleteAPI(APIView):
    def delete(self,request):
        id=request.GET.get("id")
        userdb.certificate.delete_one({"_id":ObjectId(id)})
        message="data sucessfully delete"
        return JsonResponse(message,safe=False,status=200)
              
def ceriUpdate(request):
    if 'email' in request.session:
        id=request.POST.get('id')
        
        ceriName=request.POST.get('ceriName')
        ceriName=ceriName.upper()
        ceriImage =request.FILES.get('ceriImage[]')
        ceriImage1 = request.POST.get('ceriImage1')
        ceriText = request.POST.get('ceriText')
        statusText=request.POST.get('statusText')
        if "Active " in statusText:
            status=True
        else:
            status=False
        if ceriImage is not None:
            image=cloudinary.uploader.upload(ceriImage,crop="fit",folder="unicor/ceri/")
            public_id =image['public_id']
            extension = image['format']
            img=cloudinary.CloudinaryImage(public_id,format=extension)
            img_url =img.build_url(width=122,height=26,crop="scale")
       
        else:
            img_url=ceriImage1
            
        josondata=[{
            "id":id,
            "ceriName":ceriName,
            "ceriImage":img_url,
            "ceriText":ceriText,
            "statusText":statusText,
            "status":status
        }]
        json_data={"data":josondata}
        
        requests.patch(BASE_URL+"CeriUpdateAPI/",json=json_data,verify=False)
        
        return redirect("ceri")
    else:
        del request.session["email"]
        return redirect('signin')
    
class CeriUpdateAPI(APIView):
    def patch(self,request):
        
        try:
            get_ceri = request.data
            
            for i in get_ceri['data']:
                
                
                userdb.certificate.update({'_id':ObjectId(i['id'])},{
                  '$set':{
                      'ceriName':i['ceriName'],
                      'ceriImage':i['ceriImage'],
                      'ceriText':i['ceriText'],
                      'statusText':i['statusText']
                                      
                  }  
                })
            message=[{
                'message':'Certificate sucessfully update..'
            }]
           
            sucess_message=response_messages(0,message)
            return JsonResponse(sucess_message,safe=False,status=200)
        except Exception as e:
            print("dgdgdfg",e)
            message=[{
                "message":"internal server error{0}".format(e)
            }]
            error_message=response_messages(2,message)
            return JsonResponse(message,safe=False,status=500)