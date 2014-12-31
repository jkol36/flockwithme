# -*- coding: utf-8 -*-
from threading import Thread
from django.conf import settings
from flockwithme.app.scheduler.models import OauthSet
import time
import logging
logger = logging.getLogger(__name__)

class CountDown(object):
	def __init__(self, *args, **kwargs):
		self.auth_set = kwargs.pop("auth_set")
		print self.auth_set
		start_count_down = self.start()
		return super(CountDown, self).__init__(*args, **kwargs)
		self.daemon = True

	def start(self):
		for i in range(600, -1, -1):
			time.sleep(1)
		update_oauth_set = OauthSet.objects.get(access_key=self.auth_set)
		update_oauth_set.rate_limited = False

