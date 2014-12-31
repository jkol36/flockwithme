"""
Django settings for flockwithme project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6&nk*8d**vdfddn0q(d0pa3j@!t2tl^n+j@_f3q#j=*rqheu)k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'baseflock' not in socket.gethostname()

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

#timezone
USE_TZ = True
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'flockwithme.core',
    'flockwithme.core.profiles',
    'flockwithme.core.dashboard',
    'flockwithme.core.landing',

    'flockwithme.app',
    'flockwithme.app.scheduler',
    'flockwithme.app.subscribe',
    # 'flockwithme.app.notification',
    
    'django_ajax',
    'kronos',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'flockwithme.urls'

WSGI_APPLICATION = 'flockwithme.wsgi.application'

STATIC_ROOT = '/webapps/flock_django/static'
MEDIA_ROOT = '/webapps/flock_django/uploads'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

"""
if DEBUG:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
"""


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'flock_dbase',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'flocker',
        'PASSWORD': 'StoreTheFlock',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
   

# Templates

TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'flockwithme/templates'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "flockwithme/static"),
)

AUTH_USER_MODEL = 'profiles.Profile'
SOCIAL_AUTH_USER_MODEL = 'profiles.Profile'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.me.models.DjangoStorage'
SOCIAL_AUTH_USER_MODEL = 'mongoengine.django.auth.User'


TWITTER_KEY = '3Gsg8IIX95Wxq28pDEkA'
TWITTER_SECRET = 'LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o'

Consumer_Keys = {"consumer_key1":"fYPmnEQtta3xXqS9CGhTwJf4M"}
Consumer_Secrets = {"consumer_secret1":"pVMlJRb47bYEPRrzRcGydYhcuWDwiaXPqgyDKahTtWf4tcu8A8"}
Access_Tokens = {"access_token1":"258627515-fE5flw24GC8DPVWr5EE1nAVRWKwutkZOlH4L1Z0J"}
Access_Secrets = {"access_secret1":"0fJsYMlf1KBtKCMP6RrLVxlAAuAjn34FEscVOSNSbjDO2"}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose'
        },
        'schedulefile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'scheduler.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'flockwithme.app.scheduler': {
            'handlers': ['schedulefile'],
            'level': 'DEBUG',
        },
    }
}




