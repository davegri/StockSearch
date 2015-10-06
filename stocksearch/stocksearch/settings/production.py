# -*- coding: utf-8 -*-
from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stocksearch_db',
        'USER': 'david',
        'PASSWORD': 'david',
        'HOST': '',
        'PORT': '',
    }
}


STATIC_ROOT = os.path.dirname(BASE_DIR)
STATIC_URL = '/static/'
