# -*- coding: utf-8 -*-
"""
Django settings for sita project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import datetime
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*+a9uub1)_lc7)fxhba4$%g2#&shao3o))4=_t&k7dyrr3)l47'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sita.local']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    # Models
    'sita.users',
    'sita.patients',
    'sita.cards',
    'sita.subscriptions',
    'sita.payments',
    'sita.appointments',
    'sita.notes',
    'sita.authentication',
    # Third party apps.
    'rest_framework_swagger',
    'rest_framework',
    'django_cron',
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CRON_CLASSES = [
    "sita.utils.cron.MyCronJob",
]

ROOT_URLCONF = 'sita.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.realpath(os.path.join(BASE_DIR, 'templates'))
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

AUTH_USER_MODEL = 'users.User'

WSGI_APPLICATION = 'sita.wsgi.application'


# DJango-rest-framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_PAGINATION_CLASS': (
        # Your project default_pagination class project/utils/pagination.py
        'sita.utils.pagination.ProjectDefaultPagination'
    ),
    'PAGE_SIZE': 24
}

# JWT_AUTH for jwt
JWT_AUTH = {
    'JWT_ENCODE_HANDLER': (
        'rest_framework_jwt.utils.jwt_encode_handler'
    ),
    'JWT_DECODE_HANDLER': (
        'rest_framework_jwt.utils.jwt_decode_handler'
    ),
    'JWT_PAYLOAD_HANDLER': (
        'rest_framework_jwt.utils.jwt_payload_handler'
    ),
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': (
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler'
    ),
    'VJWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1800),
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}


SWAGGER_SETTINGS = {
    'info': {
        'title': 'Swagger Sita App',
        },
}
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/assets/'

STATICFILES_DIRS = (
    os.path.realpath(os.path.join(BASE_DIR, '..', 'assets')),
)

STATIC_ROOT = os.path.realpath(
    os.path.join(BASE_DIR, '..', '..', 'media', 'assets')
)

# User uploaded files
MEDIA_ROOT = os.path.realpath(
    os.path.join(BASE_DIR, '..', '..', 'media', 'uploads')
)

MEDIA_URL = '/media/uploads/'

PRODUCTION = False

BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
