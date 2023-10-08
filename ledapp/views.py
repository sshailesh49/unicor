from django.shortcuts import render,redirect
from rest_framework import APIView
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

# Create your views here.


def response_messages(response_message,response_data):
    final_response_message ={
        "message":response_message,
        "result":response_data
    }
    return final_response_message

# sign in page
def sign_page(request):
    try:
        del request.session['email']
        del request.session['timezone']
    except:
        pass

    return render(request,'admin/login.html',context={"emptyflag":0})

#logout page

def logout(request):
    try:
        del request.session['email']
        return redirect('signin')
    except:
        del request.session['email']
        return redirect('signin')

#login page 

def login_page(request):
    if 'email' in request.session:
        del request.session['email']

    emailId =request.POST.get('email')
    print(emailId)
    password = request.POST.get('password')
    print(password)
    userDB=userdb.superadmin.find({'email':emailId,'password':password})
    print(userDB.count())
    if userDB.count() > 0:
        for user in userDB:
            request.session['email']= emailId
    
        return redirect('slider')
    else:
        return redirect('signin')


