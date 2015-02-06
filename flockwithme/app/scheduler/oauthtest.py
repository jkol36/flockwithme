# -*- coding: utf-8 -*-
import tweepy
import pickle
import datetime
import sys


class TestApi:
	def __init__(self, *args, **kwargs): 
		a, b, c, d = "3Gsg8IIX95Wxq28pDEkA", "LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o", "258627515-2YbIS6XXingGqlumiyQQTpFNTVUFrr1dNuUN79g4", "vFzKBe3HpfMuuZWyblAIHW0fIT0K17vKz4OIFxtpG8xS0"
		self.auth = tweepy.OAuthHandler(a, b)
		self.auth.set_access_token(c, d)
		self.api = tweepy.API(self.auth)
		return super(TestApi, self).__init__(*args, **kwargs)
	
	def get_remaining_follow_requests(self):
		return int(self.api.rate_limit_status()['resources']['followers']['followers/ids']['remaining'])

		

