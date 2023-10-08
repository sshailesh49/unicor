"""
Django settings for unicor project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pathlib import Path

env_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/ledapp/.env'
load_dotenv(dotenv_path=env_path)
IS_AUTH_SERVER=os.getenv("IS_AUTH_SERVER")
BASE_URL=os.getenv("BASE_URL")
APP_URL=os.getenv("APP_URL")
LED_MONGODB_URL=os.getenv("LED_MONGODB_URL")
LED_MONGODB_DATABASE_NAME=os.getenv("LED_MONGODB_DATABASE_NAME")
LED_MONGODB_USERNAME = os.getenv("LED_MONGODB_USERNAME")
LED_MONGODB_DATABASE_PASSWORD =os.getenv("LED_MONGODB_DATABASE_PASSWORD")


USER_MONGODB_URL=os.getenv("USER_MONGODB_URL")
USER_MONGODB_DATABASE_NAME=os.getenv("USER_MONGODB_DATABASE_NAME")
USER_MONGODB_USERNAME = os.getenv("USER_MONGODB_USERNAME")
USER_MONGODB_DATABASE_PASSWORD =os.getenv("USER_MONGODB_DATABASE_PASSWORD")

CLOUDINARY_NAME =os.getenv("CLOUDINARY_NAME")
CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR /"templates"
STATIC_DIR = BASE_DIR /"static"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2e5g24vwbmlnyom^#^ev!w*a0*l(vh#buc8@c#m=*qbhq&7eay'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'adminappapi',
    'ledapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'unicor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'unicor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#user Database MongoDB
client1=MongoClient("mongodb+srv://sshailesh3508:hQCHpSbxoDXh4vNN@cluster0.bknvyd6.mongodb.net/?retryWrites=true&w=majority")
userdb =client1.userdb

# app database MongoDB
client =MongoClient(LED_MONGODB_URL)
leddb = client.leddb

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS =[STATIC_DIR]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

SESSION_ENGINE = "django.contrib.sessions.backends.file"
SESSION_FILE_PATH= BASE_DIR / "session"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
