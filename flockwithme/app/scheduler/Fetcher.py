import os
import sys
from optparse import OptionParser
from django.conf import settings
import time
import tweepy
from tweepy.error import TweepError
from flockwithme.app.scheduler.models import OauthSet, Influencer, TwitterUser, TwitterRelationship, TwitterStatus, Hashtag
from flockwithme.core.profiles.models import SocialProfile
from threading import Thread

#a class with all our Twitter Get Methods
class TwitterGetFunctions(object):
	def __init__(self, socialprofile=None, influencer=None, screen_name=None, *args, **kwargs):
		self.socialprofile = socialprofile
		self.influencer = influencer
		self.screen_name = screen_name
		super(TwitterGetFunctions, self).__init__()
	
	def get_api(self):
		self.access_token = self.socialprofile.token
		self.access_token_secret = self.socialprofile.secret
		self.consumer_key = '3Gsg8IIX95Wxq28pDEkA'
		self.consumer_secret = "LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o"
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		return self.api
	
	def get_tweets(self, screen_name=None, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name:
			try:
				tweets = tweepy.Cursor(self.api.user_timeline).items(5)
			except TweepError as e:
				self.process_e = self.process_exception(e)
			for status in tweets:
				self.tstatus = self.process_status(status)
				self.socialprofile.add_tweet(self.tstatus)
			self.socialprofile.save()

				
		return tweepy.Cursor(self.api.user_timeline, screen_name=self.screen_name).items()
		
	def process_status(self, status):
		self.hashtags = [x for x in status.entities.hashtags]
		self.tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id = status.id, text=status.text.encode('utf-8'), favorite_count = status.favorite_count, retweet_count=status.retweet_count)
		self.tstatus.save()
		if not self.hashtags:
			return self.tstatus
		for hashtag in self.hashtags:
			self.h, _ = Hashtag.objects.get_or_create(name=hashtag, twitterStatus=self.tstatus) 
			self.h.save()
		return self.tstatus


	def get_followers(self, screen_name=None, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name:
			self.twitter_followers = tweepy.Cursor(self.api.followers_ids).items(5)
			for twitter_id in self.twitter_followers:
				tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
				tuser.save()
				self.socialprofile.add_follower(tuser, is_initial=self.is_initial)
				self.socialprofile.save()
			return "Done"

		self.twitter_followers = tweepy.Cursor(self.api.followers_ids, screen_name=screen_name).items()
		for twitter_id in self.twitter_followers:
			self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
			self.tuser.save()
			self.relationship, _ = TwitterRelationship.objects.get_or_create(influencer=self.influencer, twitterUser=self.Tuser, action="FOLLOWER")
			self.relationship.save()
			self.influencer.save()
		return "Done"

	def get_friends(self, screen_name=None, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name:
			self.twitter_friends = tweepy.Cursor(self.api.followers_ids).items(5)
			for twitter_id  in self.twitter_friends:
				tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
				tuser.save()
				self.socialprofile.add_friend(tuser, is_initial=self.is_initial)
				self.socialprofile.save()
			return "Done"
		self.twitter_friends = tweepy.Cursor(self.get_api.followers_ids, screen_name=self.screen_name)
		for twitter_id in self.twitter_friends:
			self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
			self.tuser.save()
			self.new_relationship = TwitterRelationship.objects.get_or_create(influencer=self.influencer, twitterUser=self.tuser, action="FRIEND", is_initial=self.is_initial)
			self.new_relationship.save()
			self.influencer.save()
		return "Done"

	def get_favorites(self, screen_name=None, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name:
			self.favorites = tweepy.Cursor(self.api.favorites).items(5)
			for status in self.favorites:
				self.Tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id=status.id, text=status.text.encode('utf-8'), favorite_count=status.favorites_count, retweet_count=status.retweet_count)
				self.Tstatus.save()
				self.socialprofile.add_favorite(self.Tstatus, is_initial=self.is_initial) 
				self.socialprofile.save()
			return "Done"
		self.favorites = tweepy.Cursor(self.api.favorites, screen_name=self.screen_name)
		for status in self.favorites:
			self.Tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id=status.id, text=status.text.encode('utf-8'), favorite_count=status.favorites_count, retweet_count=status.retweet_count)
			self.Tstatus.save()
			self.new_relationship, _ = TwitterRelationship.objects.get_or_create(twitterStatus=self.Tstatus, influencer=self.influencer, action="FAVORITE", is_initial=self.is_initial)
			self.new_relationship.save()
			self.influencer.save()
		return "Done"
	#followers, Friends, Tweets
	def get_everything(self, screen_name=None, is_initial=False):
		self.get_followers(is_initial=self.is_initial)
		self.get_friends(is_initial=self.is_initial)
		self.get_favorites(is_initial=self.is_initial)
		self.get_tweets(is_initial=self.is_initial)

		

		



	def process_exception(self, e):
		if "Rate limit exceeded" in str(e):
			print 'rate limited, sleeping'
			time.sleep(900)
		else:
			print 'error'
		
	


class FetchSocialProfileInfo(Thread, TwitterGetFunctions):
	def __init__(self, is_initial=False, *args, **kwargs):
		self.queue = kwargs.pop('queue')
		self.socialprofile = kwargs.pop('socialprofile')
		self.action = kwargs.pop('action')
		self.is_initial = is_initial
		print self.is_initial
		self.queue.put(self)
		TwitterGetFunctions.__init__(self, socialprofile=self.socialprofile,  *args, **kwargs)
		super(FetchSocialProfileInfo, self).__init__(*args, **kwargs)

	def run(self):
		if self.action == "Get_Everything":
			self.action = self.get_everything(is_initial=self.is_initial)
		elif self.action == "Get_Tweets":
			self.action = self.get_tweets(is_initial=self.is_initial)
		elif self.action == "Get_Followers":
			self.action = self.get_followers()

class FetchInfluencerInfo(Thread, TwitterGetFunctions):
	def __init__(self, *args, **kwargs):
		self.queue = kwargs.pop('queue')
		self.influencer = kwargs.pop('influencer')
		self.screen_name = kwargs.pop('screen_name')
		self.action = kwargs.pop('action')
		self.consumer_key = 'fYPmnEQtta3xXqS9CGhTwJf4M'
		self.consumer_secret = 'pVMlJRb47bYEPRrzRcGydYhcuWDwiaXPqgyDKahTtWf4tcu8A8'
		self.access_token = '258627515-fE5flw24GC8DPVWr5EE1nAVRWKwutkZOlH4L1Z0J'
		self.access_token_secret = '0fJsYMlf1KBtKCMP6RrLVxlAAuAjn34FEscVOSNSbjDO2'
		TwitterGetFunctions.__init__(self, screen_name=self.screen_name, influencer=self.influencer)
		super(FetchInfluencerInfo, self).__init__(*args, **kwargs)

	def run(self):
		if self.action == "Get_Everything":
			self.action = self.get_everything(influencer=self.influencer, screen_name=self.screen_name)

		elif self.action == "Get_Followers":
			self.action = self.get_followers(influencer=self.influencer, screen_name=self.screen_name)

		elif self.action == "Get_Tweets":
			self.action = self.get_tweets(influencer=self.influencer, screen_name=self.screen_name)

		elif self.action == "Get_Favorites":
			self.actioon = self.get_favorites(influencer=self.influencer, screen_name=self.screen_name)

		elif self.action == "Get_Friends":
			self.action = self.get_friends(influencer=self.influencer, screen_name=self.screen_name)

class FetchSocialProfileInitial(object):
	def __init__(self, *args, **kwargs):
		self.access_token = kwargs.pop('token')
		self.access_token_secret = kwargs.pop('token_secret')
		self.consumer_key = '3Gsg8IIX95Wxq28pDEkA'
		self.consumer_secret = 'LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o'
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		return super(FetchSocialProfileInitial, self).__init__(*args, **kwargs)

	def get_twitter_id(self):
		return self.api.me().id

	def get_follower_count(self):
		return self.api.me().followers_count

	def get_friend_count(self):
		return self.api.me().friends_count

