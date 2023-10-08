from django.contrib import admin
from django.urls import path


from . import views
from .viewlogics import slider,product,about,contact,social,certificate,logo,tagline,enquiry,singleproduct



urlpatterns = [

    # ---------------------adminurl---------------

    path('',views.sign_page,name="signin"),
    path('login/',views.login_page,name="login"),
    path('logout/',views.logout,name="logout"),

    path('slider/',slider.indexpage,name='slider'),
    path('slideAdd/',slider.slideAdd,name='slideAdd'),
    
    path('SliderAddAPI/',slider.SliderAddAPI.as_view(),name='SliderAddAPI'),
    path('SliderListAPI/',slider.SliderListAPI.as_view(),name='SliderListAPI'),
    path('SliderDeleteAPI/',slider.SliderDeleteAPI.as_view(),name='SliderDeleteAPI'),
    path('sliderUpdate/',slider.sliderUpdate,name='sliderUpdate'),
    path('SliderDataAPI/',slider.SliderDataAPI.as_view(),name='SliderDataAPI'),
    path('SliderUpdateAPI/',slider.SliderUpdateAPI.as_view(),name='SliderUpdateAPI'),

    path('product/',product.productPage,name='product'),
    path('productAdd/',product.productAdd,name='productAdd'),
    path('productUpdate/',product.productUpdate,name='productUpdate'),
    path('ProductAddAPI/',product.ProductAddAPI.as_view(),name='ProductAddAPI'),
    path('ProductUpdateAPI/',product.ProductUpdateAPI.as_view(),name='ProductUpdateAPI'),
    path('ProductListAPI/',product.ProductListAPI.as_view(),name='ProductListAPI'),
    path('ProductDeleteAPI/',product.ProductDeleteAPI.as_view(),name='ProductDeleteAPI'),
    path('ProductDataAPI/',product.ProductDataAPI.as_view(),name='ProductDataAPI'),
    
    
    path('about/',about.aboutpage,name='about'),
    path('AboutAddAPI/',about.AboutAddAPI.as_view(),name='AboutAddAPI'),
    path('aboutAdd/',about.aboutAdd,name='aboutAdd'),
    path('aboutUpdate/',about.aboutUpdate,name='aboutUpdate'),
    path('AboutListAPI/',about.AboutListAPI.as_view(),name='AboutListAPI'),
    path('AboutDeleteAPI/',about.AboutDeleteAPI.as_view(),name='AboutDeleteAPI'),
    path('AboutUpdateAPI/',about.AboutUpdateAPI.as_view(),name='AboutUpdateAPI'),
    path('AboutDataAPI/',about.AboutDataAPI.as_view(),name='AboutDataAPI'),
    
     # ------------------- Contact-----------------------
    path('contact/',contact.ContactPage, name="contact"),
    path('contactAdd/',contact.contactAdd,name='contactAdd'),
    path('ContactAddAPI/',contact.ContactAddAPI.as_view(),name ='ContactAddAPI'),
    path('ContactListAPI/',contact.ContactListAPI.as_view(),name ='ContactListAPI'),
    path('ContactDeleteAPI/',contact.ContactDeleteAPI.as_view(),name ='ContactDeleteAPI'),
    path('ContactDataAPI/',contact.ContactDataAPI.as_view(),name='ContactDataAPI'),
    path('contactUpdate/',contact.contactUpdate,name='contactUpdate'),
    path('ContactUpdateAPI/',contact.ContactUpdateAPI.as_view(),name='ContactUpdateAPI'),
    path('ContactUpdateAPI/',contact.ContactUpdateAPI.as_view(),name='ContactUpdateAPI'),
    path('EnquiryListAPI/',enquiry.EnquiryListAPI.as_view(),name='EnquiryListAPI'),
    path('enquiry/',enquiry.EnquiryPage,name='enquiry'),
    
    
    
    
    path('social/',social.SocialPage,name='social'),
    path('SocialAddAPI/',social.SocialAddAPI.as_view(),name='SocialAddAPI'),
    path('socialAdd/',social.socialAdd,name='socialAdd'),
    path('socialUpdate/',social.socialUpdate,name='socialUpdate'),
    path('SocialListAPI/',social.SocialListAPI.as_view(),name='SocialListAPI'),
    path('SocialDeleteAPI/',social.SocialDeleteAPI.as_view(),name='SocialDeleteAPI'),
    path('SocialUpdateAPI/',social.SocialUpdateAPI.as_view(),name='SocialUpdateAPI'),
    path('SocialDataAPI/',social.SocialDataAPI.as_view(),name='SocialDataAPI'),
    
    
    path('logo/',logo.logopage,name='logo'),
    path('logoAdd/',logo.logoAdd,name='logoAdd'),
    path('logoUpdate/',logo.logoUpdate,name='logoUpdate'),
    path('LogoAddAPI/',logo.LogoAddAPI.as_view(),name='LogoAddAPI'),
    path('LogoListAPI/',logo.LogoListAPI.as_view(),name='LogoListAPI'),
    path('LogoDeleteAPI/',logo.LogoDeleteAPI.as_view(),name='LogoDeleteAPI'),
    path('LogoUpdateAPI/',logo.LogoUpdateAPI.as_view(),name='LogoUpdateAPI'),
    path('LogoDataAPI/',logo.LogoDataAPI.as_view(),name='LogoDataAPI'),
    
    
    
    
    path('ceri/',certificate.certificatePage,name='ceri'),
    path('ceriAdd/',certificate.ceriAdd,name='ceriAdd'),
    path('ceriUpdate/',certificate.ceriUpdate,name='ceriUpdate'),
    path('CeriAddAPI/',certificate.CeriAddAPI.as_view(),name='CeriAddAPI'),
    path('CeriListAPI/',certificate.CeriListAPI.as_view(),name='CeriListAPI'),
    path('CeriDeleteAPI/',certificate.CeriDeleteAPI.as_view(),name='CeriDeleteAPI'),
    path('CeriUpdateAPI/',certificate.CeriUpdateAPI.as_view(),name='CeriUpdateAPI'),
    path('CeriDataAPI/',certificate.CeriDataAPI.as_view(),name='CeriDataAPI'),
     
    path('tag/',tagline.taglinePage,name='tag'),
    path('taglineAdd/',tagline.taglineAdd,name='taglineAdd'),
    path('tagUpdate/',tagline.taglineUpdate,name='tagUpdate'),
    path('TaglineAddAPI/',tagline.TaglineAddAPI.as_view(),name='TaglineAddAPI'),
    path('TaglineListAPI/',tagline.TaglineListAPI.as_view(),name='TaglineListAPI'),
    path('TaglineDeleteAPI/',tagline.TaglineDeleteAPI.as_view(),name='TaglineDeleteAPI'),
    path('TaglineUpdateAPI/',tagline.TaglineUpdateAPI.as_view(),name='TaglineUpdateAPI'),
    path('TaglineDataAPI/',tagline.TaglineDataAPI.as_view(),name='TaglineDataAPI'),
    
    
    path('singleadmin/',singleproduct.singlePage,name='singleadmin'),
    path('SingleProductAddAPI/',singleproduct.SingleProductAddAPI.as_view(),name='SingleProductAddAPI'),
    path('singleAdd/',singleproduct.singleAdd,name='singleAdd'),
    path('singleUpdate/',singleproduct.singleUpdate,name='singleUpdate'),
    path('SingleProductListAPI/',singleproduct.SingleProductListAPI.as_view(),name='SingleProductListAPI'),
    path('SingleProductDeleteAPI/',singleproduct.SingleProductDeleteAPI.as_view(),name='SingleProductDeleteAPI'),
    path('SingleProductUpdateAPI/',singleproduct.SingleProductUpdateAPI.as_view(),name='SingleProductUpdateAPI'),
    path('SingleProductDataAPI/',singleproduct.SingleProductListAPI.as_view(),name='SingleProductListAPI'),
     

    




    
]