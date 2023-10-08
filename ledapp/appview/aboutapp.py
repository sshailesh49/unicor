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
    '''

    '''
    final_response_message = {
        "message": response_message,
        "result": response_data
    }
    return final_response_message

#  --------------------------Main website Views----------------------------


def aboutApp(request):
    return render(request, 'app/about.html')


def homeApp(request):
    return render(request, 'app/index.html')


def productApp(request):
    return render(request, 'app/products.html')


def contactApp(request):
    return render(request, 'app/contact.html')

def singleProductApp(request):
    return render(request, 'app/single-product.html')




class AboutAppAPI(APIView):
    def get(self, request):
        try:
            get_about = userdb.about.find({}).sort('createdOn', -1).limit(1)

            about = []
            for i in get_about:

                i['id'] = str(i['_id'])
                del i['_id']
                about.append(i)

            return JsonResponse(about, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class CeriAppAPI(APIView):
    def get(self, request):
        try:
            get_ceri = userdb.certificate.find(
                {}).sort('createdOn', -1).limit(1)

            ceri = []
            for i in get_ceri:

                i['id'] = str(i['_id'])

                del i['_id']
                ceri.append(i)

            return JsonResponse(ceri, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class LogoAppAPI(APIView):
    def get(self, request):
        try:
            get_ceri = userdb.logo.find({}).sort('createdOn', -1).limit(1)

            ceri = []
            for i in get_ceri:

                i['id'] = str(i['_id'])

                del i['_id']
                ceri.append(i)

            return JsonResponse(ceri, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class ContactAppAPI(APIView):
    def get(self, request):
        try:
            get_ceri = userdb.contact.find({}).sort('createdOn', -1).limit(1)

            ceri = []
            for i in get_ceri:

                i['id'] = str(i['_id'])

                del i['_id']
                ceri.append(i)

            return JsonResponse(ceri, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class BannerAppAPI(APIView):
    def get(self, request):
        try:
            get_ceri = userdb.slider.find({}).sort('createdOn', -1).limit(1)

            ceri = []
            for i in get_ceri:

                i['id'] = str(i['_id'])

                del i['_id']
                ceri.append(i)

            return JsonResponse(ceri, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class TaglineAppAPI(APIView):
    def get(self, request):
        try:
            get_data = userdb.tagline.find({}).sort('createdOn', -1).limit(1)

            tag = []
            for i in get_data:

                i['id'] = str(i['_id'])

                del i['_id']
                tag.append(i)

            return JsonResponse(tag, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class SocialAppAPI(APIView):
    def get(self, request):
        try:
            get_data = userdb.social.find({}).sort('createdOn', -1).limit(1)

            social = []
            for i in get_data:

                i['id'] = str(i['_id'])

                del i['_id']
                social.append(i)

            return JsonResponse(social, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)


class ProductAppAPI(APIView):
    def get(self, request):
        try:
            get_data = userdb.product.find({}).sort('createdOn', -1)

            product = []
            for i in get_data:

                i['id'] = str(i['_id'])

                del i['_id']
                product.append(i)

            return JsonResponse(product, safe=False, status=200)
        except Exception as e:
            message = "Internal server error{0}".format(e)
            return JsonResponse(message, safe=False, status=500)
