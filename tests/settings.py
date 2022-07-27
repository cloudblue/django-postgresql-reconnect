#
#  Copyright © 2022 Ingram Micro Inc. All rights reserved.
#

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '6^1@%4#qtc+bookwp4w5k-+nbo+clm!skzdhnyl@rf&06b5tl6'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
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

DATABASES = {
    'default': {
        'ENGINE': 'django_postgresql_reconnect.backend',
        'NAME': 'django_postgresql_reconnect',
        'USER': 'postgres',
        'PASSWORD': '1q2w3e',
        'HOST': 'db_ram',
        'RECONNECT': True,
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
