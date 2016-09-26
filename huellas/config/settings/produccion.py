from .base import *
from .installed_apps import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'huellas',
        'USER': 'huellas',
        'PASSWORD': 'huellas',
        'HOST': 'localhost',
    }
}