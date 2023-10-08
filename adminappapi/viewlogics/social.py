from logging import exception
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



def SocialPage(request):
    if 'email' in request.session:
        return render(request,'admin/social_form.html')
    else:
        return redirect('signin')
    
    
def socialAdd(request):
    if 'email' in request.session:
        #token = request.session['accessToken']

        #headers = {"Authorization": token}
        id = []
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        youtube = request.POST.get('youtube')
        statusText=request.POST.get('statusText')
        

        if   "Active" in statusText :
            status=True
        else:
            status=False
            
        jsondata_submit = [{"facebook":facebook,
                            "instagram":instagram,
                            "twitter" : twitter,
                            "youtube" : youtube,
                            "status":status,
                            "statusText":statusText,
                            "createdBy":request.session['email'],
                            "createdOn":datetime.now().timestamp()
                           }]
        json_data = {"data": jsondata_submit}
        get_all_social = requests.post(BASE_URL + "SocialAddAPI/", json=json_data)
        if get_all_social.status_code == 404:
            msg=get_all_social.json()
            return redirect('/adminpanel/social/')
        elif get_all_social.status_code == 500:
            return render(request, 'admin/error500.html')
        elif get_all_social.status_code == 200:
            msg=get_all_social.json()
            return redirect('/adminpanel/social/')
        elif get_all_social.status_code == 401:
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')


class SocialAddAPI(APIView):
    def post(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            get_social = request.data
            for i in get_social['data']:
                print("---------------",i)
               
                userdb.social.insert(i)
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



class SocialListAPI(APIView):
  

    def get(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            #id = request.GET.get('id')
            
            social = []
            get_social = userdb.social.find({})
            for i in get_social:
                social.append({
                    'id': str(i['_id']),
                    'facebook': i['facebook'],
                    'instagram': i['instagram'],
                    'twitter': i['twitter'],
                    'youtube': i['youtube'],
                    'status': i['statusText'],
                   
                    
                    
                })
            return JsonResponse(social, safe=False, status=200)
        except:
            message = [
                {
                    "message": "Internal Server Error"
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)






class SocialDataAPI(APIView):
    '''
    API for Particular User Subscribe Channel
    '''

    def get(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            id = request.GET.get('id')
            social = []
            get_social = userdb.social.find({"_id": ObjectId(id)})
            
            for i in get_social:
               # print("23232",i['facebook'])
                social.append({
                    'id': str(i['_id']),
                    'facebook':i['facebook'],
                    'instagram':i['instagram'],
                    'twitter': i['twitter'],
                    'youtube': i['youtube'],
                    
                    
                })
            return JsonResponse(social, safe=False, status=200)
        except Exception as e:
            message = [
                {
                    "message": "Internal Server Error{e}".format(0)
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)



class SocialDeleteAPI(APIView):
    
    def delete(self, request):
        # try:
        #token = request.META['HTTP_AUTHORIZATION']
        id=request.GET.get('id')
       
        userdb.social.delete_one({'_id':ObjectId(id)})
        message = [
                {
                    "message": "Social link SuccessFully Removed"
                }
            ]
        success_message = response_messages(0, message)
        return JsonResponse(success_message, safe=False, status=200)
    
def socialUpdate(request):
    if 'email' in request.session:
        id=request.POST.get('id')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        youtube = request.POST.get('youtube')
        statusText =request.POST.get('statusText')
        
        if "Active" in statusText:
            status=True
        else:
            status=False
        jsondata_submit =[
            {
                'id':id,
                'facebook':facebook,
                'instagram':instagram,
                'twitter':twitter,
                'youtube':youtube,
                'status':status,
                'statusText':statusText
                
            }]
        json_data ={"data":jsondata_submit}
        requests.patch(BASE_URL+"SocialUpdateAPI/",json=json_data,verify=False)
        return redirect('social')
    else:
        del request.session['email']
        return redirect("/signin/")
    
class SocialUpdateAPI(APIView):
    def patch(self,request):
        try:
            get_social =request.data
            for i in get_social['data']:
                userdb.social.update(
                    {'_id':ObjectId(i['id'])},
                    {'$set':{
                        
                        'facebook':i['facebook'],
                        'instagram':i['instagram'],
                        'twitter':i['twitter'],
                        'youtube':i['youtube'],
                        'status':i['status'],
                        'statusText':i['statusText']
                        
                    }
                   })
                message=[{
                    'message':'Social Link Updated'
                }]
            success_message =response_messages(0,message)
            return JsonResponse(success_message,safe=False,status=200)
        
            
        
        except Exception as e:
            message=[{
                
                "message":"internal server error{0}".format(e)
            }]
        error_message = response_messages(2,message)
        return JsonResponse(error_message,safe=False,status=500)
    
    
    

               
        