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


from unicor.settings import userdb, IS_AUTH_SERVER, CLOUDINARY_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, BASE_URL,APP_URL
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


def EnquiryPage(request):
    if 'email' in request.session:
        return render(request, 'admin/enquiry_form.html')
    else:
        return redirect('signin')





class EnquiryListAPI(APIView):

    def get(self, request):
        try:
            #token = request.META['HTTP_AUTHORIZATION']

            #id = request.GET.get('id')

            enquiry = []
            get_enquiry = userdb.enquiry.find({})
           
            for i in get_enquiry:
               
                enquiry.append({
                            'id': str(i['_id']),
                            'name': i['name'],
                            'mobile': i['mobile'],
                            'email': i['email'],
                            'message':i['message'],
                            'createdOn':str(i['createdOn'])


                })
            return JsonResponse(enquiry, safe=False, status=200)
        except:
            message = [
                {
                    "message": "Internal Server Error"
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)


class CategoryBusinessData(APIView):
    '''
    API for Particular User Subscribe Channel
    '''

    def get(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION']

            id = request.GET.get('id')
            category = []
            get_posts = db.bussinessCategories.find({"_id": ObjectId(id)})
            for i in get_posts:
                category.append({
                    'Id': str(i['_id']),
                    'categoryName': i['type']
                })
            return JsonResponse(category, safe=False, status=200)
        except:
            message = [
                {
                    "message": "Internal Server Error"
                }
            ]
            error_message = response_messages(2, message)
            return JsonResponse(error_message, safe=False, status=500)


class EnquiryDeleteAPI(APIView):

    def delete(self, request):
        # try:
        #token = request.META['HTTP_AUTHORIZATION']
        id = request.GET.get('id')

        userdb.enquiry.delete_one({'_id': ObjectId(id)})
        message = [
            {
                "message": "Contact  SuccessFully Removed"
            }
        ]
        success_message = response_messages(0, message)
        return JsonResponse(success_message, safe=False, status=200)
