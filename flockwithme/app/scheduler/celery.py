"""
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

#set the default setting module for the celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flockwithme.settings')
app = Celery('Flockwithme')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.task(bind=True)

def debug_task(self):
	print('Request: {0!r}'.format(self.request))
"""
