# -*- coding: utf-8 -*-
"""
Django development settings for sita project.
"""
from . import *  # noqa


# Debug
DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG


# Application definition
INSTALLED_APPS += (
    'debug_toolbar',
)


MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sita',
        'USER': 'vagrant'
    }
}


# Debug toolbar
INTERNAL_IPS = ('127.0.0.1',)
