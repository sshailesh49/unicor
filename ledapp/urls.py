from django.contrib import admin
from django.urls import path
#from . import views
from .appview import aboutapp,enquiryapp



urlpatterns = [

    # ---------------------adminurl---------------

    path('abouts/',aboutapp.aboutApp,name="abouts"),
    path('AboutAppAPI/',aboutapp.AboutAppAPI.as_view(),name="AboutAppAPI"),
    path('CeriAppAPI/',aboutapp.CeriAppAPI.as_view(),name="CeriAppAPI"),
    path('LogoAppAPI/',aboutapp.LogoAppAPI.as_view(),name="LogoAppAPI"),
    path('ContactAppAPI/',aboutapp.ContactAppAPI.as_view(),name="ContactAppAPI"),
    path('BannerAppAPI/',aboutapp.BannerAppAPI.as_view(),name='BannerAppAPI'),
    path('',aboutapp.homeApp,name='homeApp'),
    path('TaglineAppAPI/',aboutapp.TaglineAppAPI.as_view(),name='TaglineAppAPI'),
     path('SocialAppAPI/',aboutapp.SocialAppAPI.as_view(),name='SocialAppAPI'),
     path('ProductAppAPI/',aboutapp.ProductAppAPI.as_view(),name='ProductAppAPI'),
     
    path('products/',aboutapp.productApp,name='products'),
    path('contactus/',aboutapp.contactApp,name='contactus'),
    path('single/',aboutapp.singleProductApp,name='single'),
    path('enquiryAdd/',enquiryapp.enquiryAdd,name='enquiryapp'),
    path('EnquiryAddAPI/',enquiryapp.EnquiryAddAPI.as_view(),name="EnquiryAddAPI")
    
  
     
    
    ]