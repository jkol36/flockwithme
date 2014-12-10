# -*- coding: utf-8 -*-
from threading import Thread
from django.conf import settings
from flockwithme.app.scheduler.models import OauthSet
import tweepy
import time
import random
import logging
logger = logging.getLogger(__name__)

class AccountFetch(Thread):
	def __init__(self, *args, **kwargs):
		self.jobs = kwargs.pop('jobs')
		print self.jobs
		self.account = kwargs.pop("account")
		print self.account
		self.queue = kwargs.pop("queue")
		self.api = self.get_api()
		return super(AccountFetch, self).__init__(*args, **kwargs)

	def on_follower(self):
		pass

	def get_api(self):
		pass
	def on_following(self):
		pass

	def on_error(self):
		pass

	def IsAlive(self):
		pass

