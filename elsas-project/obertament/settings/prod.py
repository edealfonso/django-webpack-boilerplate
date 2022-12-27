from .base import *

import mimetypes

mimetypes.add_type("text/css", ".css", True)


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ['contemporaryartnow.com', 'www.contemporaryartnow.com']

CSRF_TRUSTED_ORIGINS = ['https://contemporaryartnow.com', 'https://www.contemporaryartnow.com']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME_PROD'),
        'USER': get_secret('USER_PROD'),
        'PASSWORD': get_secret('PASSWORD_PROD'),
        'HOST': 'localhost',
        'PORT': get_secret('DB_PORT'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# custom
STATICFILES_DIRS = [BASE_DIR.child('static'),]
STATIC_ROOT = BASE_DIR.child('staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')

