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


def ContactPage(request):
    if 'email' in request.session:
        return render(request, 'admin/contactus_form.html')
    else:
        return redirect('signin')


def contactAdd(request):
    if 'email' in request.session:
        #token = request.session['accessToken']

        #headers = {"Authorization": token}
        id = []
        telephone = request.POST.get('telephone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        email = request.POST.get('email')
       # contactImage = request.FILES.get('contactImage[]')
        statusText = request.POST.get('statusText')

        #if contactImage is not None:
         #   image = cloudinary.uploader.upload(
         #       contactImage, width=300, height=300, crop='limit', folder="DharPainting/contact/")
          #  image_url = image['url']
          #  print("777777-------",image_url)
       # else:
         #   image_url = ''
         #   print("8888-------",image_url)

        if "Active" in statusText:
            status = True
        else:
            status = False

        jsondata_submit = [{"telephone": telephone,
                            "address1": address1,
                            "address2": address2,
                            "email":email,
                            #"contactImage": image_url,
                            "status": status,
                            "statusText": statusText,
                            "createdBy": request.session['email'],
                            "createdOn":datetime.now().timestamp()
                            }]
        json_data = {"data": jsondata_submit}
        get_all_contact = requests.post(
            BASE_URL + "ContactAddAPI/", json=json_data)
        if get_all_contact.status_code == 404:
            return redirect('contact')
        elif get_all_contact.status_code == 500:
            return render(request, 'admin/error500.html')
        elif get_all_contact.status_code == 200:
            return redirect('contact')
        elif get_all_contact.status_code == 401:
            return redirect('signin')
    else:
        del request.session['email']
        return redirect('signin')


class ContactAddAPI(APIView):
    def post(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            get_contact = request.data
            for i in get_contact['data']:
                contactDB = userdb.contact.find(
                    {'address1': i['address1'], "status": True})
                if contactDB.count() > 0:
                    message = [
                        {
                            "message": "contact  Exist"
                        }
                    ]
                    error_message = response_messages(1, message)
                    return JsonResponse(error_message, safe=False, status=404)
                else:
                    userdb.contact.insert(i)
                message = [
                    {
                        "message": "Contact SuccessFully Added"
                    }
                ]
                success_message = response_messages(0, message)
                return JsonResponse(success_message, safe=False, status=200)
        except:
            message = [
                {
                    "message": "Internal Server Error"
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)


class ContactListAPI(APIView):

    def get(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            #id = request.GET.get('id')

            contact = []
            get_contact = userdb.contact.find({})
            #print("-------------------",get_contact)
            for i in get_contact:
               # print("1211-----------",i['contact1'])
                contact.append({
                    'id': str(i['_id']),
                    'telephone': i['telephone'],
                    'address1': i['address1'],
                    'address2': i['address2'],
                    'email': i['email'],
                    #'contactImage': i['contactImage'],
                    'status': i['statusText'],
                    'createdBy': i['createdBy'],


                })
            return JsonResponse(contact, safe=False, status=200)
        except:
            message = [
                {
                    "message": "Internal Server Error"
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)



                 


class ContactDeleteAPI(APIView):

    def delete(self, request):
        # try:
        #token = request.META['HTTP_AUTHORIZATION']
        id = request.GET.get('id')

        userdb.contact.delete_one({'_id': ObjectId(id)})
        message = [
            {
                "message": "Contact  SuccessFully Removed"
            }
        ]
        success_message = response_messages(0, message)
        return JsonResponse(success_message, safe=False, status=200)
    
    
    
class ContactDataAPI(APIView):
    def get(self,request):
        try:
            id=request.GET.get('id')
            contact=[]
            
            get_contact= userdb.contact.find({'_id':ObjectId(id)})
            for i in get_contact:
                contact.append({
                       'id':str(i['_id']),
                       'telephone':i['telephone'],
                       'address1':i['address1'],
                       'address2' :i['address2'],
                       'email':i['email'],
                       
                        } )
            return JsonResponse(contact,safe=False,status=200)
        except Exception as e:
            message=[{
                
                "message":"internal server error...{0}".format(e)
            }]
            error_message =response_messages(2,message)
    
def contactUpdate(request):
    if 'email' in request.session:
        id=request.POST.get('id') 
        telephone = request.POST.get('telephone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        email = request.POST.get('email')
        statusText = request.POST.get('statusText')
        print("status123",statusText)
        
        if statusText == 'Active':
            status=True
            print("status2",status)
            
            
        else:
            status =False
            
        jsondata_submit=[{
            'id':id,
            'telephone':telephone,
            'address1':address1,
            'address2':address2,
            'email':email,
            'status':status,
            'statusText':statusText
            }]
        
        json_data ={'data': jsondata_submit}
        requests.patch(BASE_URL + "ContactUpdateAPI/", json=json_data, verify=False)
        return redirect('contact')
    else:
        del request.session['email']
        return redirect("/signin/")
    
    
    
class ContactUpdateAPI(APIView):
    def patch(self,request):
        try:
            get_contact = request.data
            for i in get_contact['data']:
                userdb.contact.update({'_id':ObjectId(i['id'])},
                                      {'$set':
                                          {
                                      'telephone':i['telephone'],
                                      'address1':i['address1'],
                                      'address2':i['address2'],
                                      'email':i['email'],
                                      'status':i['status'],
                                      'statusText':i['statusText']
                                         
                                          
                                       } })
                
                message=[
                    {'message':"Contact successfully update"}
                ]
            success_message=response_messages(0,message) 
            return JsonResponse(success_message,safe=False,status=200)   
        except Exception as e:
            message =[
                {"message":"internal server error{0}".format(e)
                 } ]
            error_message = response_messages(2,message)
            return JsonResponse(error_message,safe=False,status=500)
    
     
    