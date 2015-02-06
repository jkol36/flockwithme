# -*- coding: utf-8 -*-
import tweepy
import pickle
import datetime
import sys

from flockwithme.app.scheduler.models import TwitterStatus


class TestApi:
	def __init__(self, *args, **kwargs): 
		a, b, c, d = "BxJkSE7u9mAwCQOFTw", "by2ySr9AZn5T1tHgJjjlgtjajbzKu3Hv2UyBZ3FPhk", "940923151-r2r7VeVwtWMZPwoaVco7hIMt7yKEnDsvzS5SQvy5", "h65NCnGdfcR0gO04xm1O7tQcTSQnzPBpcwnQhpyTc3sdh"
		self.auth = tweepy.OAuthHandler(a, b)
		self.auth.set_access_token(c, d)
		self.api = tweepy.API(self.auth)
		
	
	def get_remaining_follow_requests(self):
		return int(self.api.rate_limit_status()['resources']['followers']['/followers/ids']['remaining'])

	def get_remaining_favorite_request(self):
		return int(self.api.rate_limit_status()['resources']['favorites']['/favorites/list']['remaining'])
		

	def favorite_tweets(self):
		print self.api.me()
		self.tweets = [x.twitter_id for x in TwitterStatus.objects.filter()[:30]]
		for tweet in self.tweets:
			self.api.create_favorite(tweet)
			print "favorited"
			return

