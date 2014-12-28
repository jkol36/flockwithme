#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from optparse import OptionParser
import tweepy
import time

class Streamer(tweepy.StreamListener):

	def __init__(self, *args, **kwargs):
		self.hashtags = kwargs.pop('hashtags')
		self.checker = time.time()
		return super(Streamer, self).__init__(*args, **kwargs)

	def on_status(self, status):
		self.process_status(status)
		return self.should_continue()

	def on_error(self, error):
		print error
		return self.should_continue()

	def on_timeout(self):
		print 'timed out'
		return self.should_continue()

	def should_continue(self):
		if time.time() - self.checker > 120:
			self.checker = time.time()
			return set(Hashtag.objects.filter(profiles__isnull=False)) == set(self.hashtags)
		return True

	def is_good(self, user):
		if user.default_profile_image:
			return False
		if not user.description or 'bot' in user.description:
			return False
		if user.followers_count < 50:
			return False
		if user.friends_count < 50:
			return False
		if int(user.friends_count) / float(user.followers_count) > 3:
			return False
		if not user.name:
			return False
		return True



	def process_status(self, status):
		user, _ = TwitterUser.objects.get_or_create(twitter_id=status.user.id)
		if not self.is_good(status.user):
			user.delete()
			return True
		user.screen_name = status.user.screen_name.encode('utf-8')
		user.favorites_count = status.user.favourites_count
		user.followers_count = status.user.followers_count
		user.friends_count = status.user.friends_count
		user.verified = status.user.verified
		user.location = status.user.location.encode('utf-8')
		user.statuses_count = status.user.statuses_count
		user.save()

		mstatus = TwitterStatus()
		mstatus.twitter_id = status.id
		mstatus.text = status.text.encode('utf-8')
		mstatus.twitter_user = user
		mstatus.favorite_count = status.favorite_count
		mstatus.retweet_count = status.retweet_count
		mstatus.save()
		for d in status.entities['hashtags']:
			hashtag, _ = Hashtag.objects.get_or_create(name=d['text'].lstrip('#').lower())
			mstatus.hashtags.add(hashtag)
		mstatus.save()




class Worker:
	def __init__(self):
		apikey = 'moX6M9jbbIuAnYuaAxZJFkzQY'
		apisecret = 'YhH1Fgr4VUyzLsKoKKQrR0bRuPbsqP4daiiZ9UbbSyZWDCsTxU'
		access_token = '1177046514-QVUDUBANp0p2HHiJrBJIwYXyaqjZkQg7NMHSRwA'
		access_secret = 'gBDQ3Z2wNGMOptyAsLffOHksIbhYlL6RvbCYSHzkWV08s'
		self.auth = tweepy.OAuthHandler(apikey, apisecret)
		self.auth.set_access_token(access_token, access_secret)

	def stream(self):
		while 1:
			hashtags = Hashtag.objects.filter(profiles__isnull=False).distinct()
			if not hashtags:
				time.sleep(10)
			stream = tweepy.Stream(self.auth, Streamer(hashtags=hashtags))
			stream.filter(track=['#'+h.name for h in hashtags], languages=['en',])
 
 
if __name__ == '__main__':
	usage = "usage: %prog -s PATH | --path=PATH"
	parser = OptionParser(usage)
	parser.add_option('-s', '--path', dest='path', metavar='PATH', help="The path to the Django environment")
	(options, args) = parser.parse_args()
	if not options.path:
		parser.error("Specify the path where manage.py is")
 
	os.environ['DJANGO_SETTINGS_MODULE'] = "flockwithme.settings"
	sys.path.append(options.path)
	
	
	####################### IMPORTS ########################
	from flockwithme.app.scheduler.models import Hashtag, TwitterUser, TwitterStatus
	########################################################
	a = Worker()
	a.stream()