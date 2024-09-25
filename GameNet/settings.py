"""
Django settings for GameNet project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2txu9cxrxb(wb3zv*4c5duy=ny%tivpzrw+c1r%ss2e+hdk9_x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','gamenet.herokuapp.com', '0.0.0.0']

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000/', 'https://gamenet.herokuapp.com/', 'http://0.0.0.0:5000/']

# Application definition

INSTALLED_APPS = [
    'games.apps.GamesConfig',
    'news.apps.NewsConfig',
    'reviews.apps.ReviewsConfig',
    'accounts.apps.AccountsConfig',
    'moderation.apps.ModerationConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django_ckeditor_5',
    'cloudinary',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_bootstrap4',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'GameNet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join("templates")],
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

WSGI_APPLICATION = 'GameNet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SITE_ID = 2

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


#Confirmation email

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587

#Media

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'media'),
]

cloudinary.config( 
  cloud_name = os.environ.get("cloud_name"), 
  api_key = os.environ.get("api_key"), 
  api_secret = os.environ.get("api_secret") 
)


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "any"  # Possible values: "staff", "authenticated", "any"

CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'png', 'gif'] # optional
CKEDITOR_5_CONFIGS = {
  'default': {
      'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                  'bulletedList', 'numberedList', 'blockQuote', 'imageUpload'],
      'language': 'pl',
  },
}
