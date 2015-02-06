# -*- coding: utf-8 -*-
import tweepy
import pickle
import datetime
import sys


class TestApi:
	def __init__(self, *args, **kwargs): 
		a, b, c, d = "3Gsg8IIX95Wxq28pDEkA", "LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o", "131687768-oQ77P6uNEUfQdRVZvOIg6pzZJb8CcZMyZzbnAqQ9", "K0HWSYtpvrgq5buCwYT6jm9dI2qf5XaX97PRyn9WyvTgs"
		self.auth = tweepy.OAuthHandler(a, b)
		self.auth.set_access_token(c, d)
		self.api = tweepy.API(self.auth)
		#return super(TestApi, self).__init__(*args, **kwargs)
		print dir(self.api)

