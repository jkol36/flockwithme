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


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


if DEBUG:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'Flock',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'Jon',
            'PASSWORD': 'J0nnyb0y123',
            'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }
    STATIC_ROOT = '/webapps/flock_django/static'
    MEDIA_ROOT = '/webapps/flock_django/uploads'

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


TWITTER_KEY = 'G3uP1GqVicL1l76NyoLvXYA8p'
TWITTER_SECRET = 'lPbzRLGrJycomcQs0V1EJ9o8NhvwwB3kn961RadKTxb7uwS8mZ'


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




