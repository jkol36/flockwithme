# -*- coding: utf-8 -*-
import tweepy
import pickle
import datetime
import sys

from flockwithme.app.scheduler.models import TwitterStatus


class TestApi:
	def __init__(self, *args, **kwargs): 
		a, b, c, d = "1srzVhteaXkb5w9bDmcUS7pBz", "LE3UDy0BHCzpazGdlWTT1TK6BqZoSZDixq4F4vLsV6NsFD7Mx5", "258627515-pAL3ygDa5wmRJk6Sehu55eLLmJCd4YgpftedwqCY", "G78SmqVENFKB7J8POHftz4WghrONvvkxXgb5xeDBK0jqt"
		self.auth = tweepy.OAuthHandler(a, b)
		self.auth.set_access_token(c, d)
		self.api = tweepy.API(self.auth)
		
	
	def get_remaining_follow_requests(self):
		return int(self.api.rate_limit_status()['resources']['followers']['/followers/ids']['remaining'])

	def get_remaining_favorite_request(self):
		return int(self.api.rate_limit_status()['resources']['favorites']['/favorites/list']['remaining'])
		

	def favorite_tweets(self):
		self.tweets = [x.twitter_id for x in TwitterStatus.objects.filter()[:30]]
		for tweet in self.tweets:
			self.api.create_favorite(tweet)
			print "favorited"
			return

