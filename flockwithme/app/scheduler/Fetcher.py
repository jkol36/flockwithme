import os
import sys
import time
from optparse import OptionParser

from django.conf import settings
import tweepy
from tweepy.error import TweepError
from threading import Thread
from django.db.models import Q

from flockwithme.app.scheduler.models import OauthSet, Influencer, TwitterUser, TwitterRelationship, TwitterStatus, Hashtag
from flockwithme.core.profiles.models import SocialProfile
from .auto_pilot import OnTweet


#a class with all our Twitter Get Methods
class TwitterGetFunctions(object):
	def __init__(self, socialprofile=None, influencer=None, screen_name=None, *args, **kwargs):
		self.socialprofile = socialprofile
		self.influencer = influencer
		self.screen_name = screen_name
		super(TwitterGetFunctions, self).__init__()
	
	def get_api(self):
		if not self.socialprofile:
			self.access_token = self.access_token
			print self.access_token
			self.access_token_secret = self.access_token_secret
			print self.access_token_secret
			self.consumer_key = self.consumer_key
			print self.consumer_key
			self.consumer_secret = self.consumer_secret
			print self.consumer_secret
		else:
			self.access_token = self.socialprofile.token
			self.access_token_secret = self.socialprofile.secret
			self.consumer_key = '3Gsg8IIX95Wxq28pDEkA'
			self.consumer_secret = "LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o"
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		return self.api
	
	def get_follower_count(self, screen_name=None, influencer=None):
		self.api = self.get_api()
		if not self.screen_name:
			return self.api.me().followers_count
		else:
			return self.api.get_user(screen_name=self.screen_name).followers_count

	def get_friends_count(self, screen_name=None, influencer=None):
		self.api = self.get_api()
		if not self.screen_name:
			return self.api.me().friends_count
		else:
			return self.api.get_user(screen_name=self.screen_name).friends_count

	def get_tweet_count(self, screen_name=None, influencer=None):
		self.api = self.get_api()
		if not self.screen_name:
			return self.api.me().statuses_count
		else:
			return self.api.get_user(screen_name=self.screen_name).statuses_count

	def get_tweets(self, screen_name=None, influencer=None, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name and is_initial == True:
			try:
				tweets = tweepy.Cursor(self.api.user_timeline).items()
			except TweepError as e:
				self.process_e = self.process_exception(e)
			try:
				for status in tweets:
					self.tstatus = self.process_status(status)
					self.socialprofile.add_tweet(self.tstatus, is_initial=self.is_initial)
			except TweepError, e:
				self.process_exception(e)
			self.socialprofile.save()
			return "Done"
		elif not self.screen_name and is_initial == False:
			self.db_tweets = [x.twitterStatus.twitter_id for x in TwitterRelationship.objects.filter(action="TWEET", socialProfile=self.socialprofile)]
			print "db tweet ids"
			print self.db_tweets
		###INFLUENCER TWEET FETCH ####
		try:
			tweets = tweepy.Cursor(self.api.user_timeline, screen_name=self.screen_name).items()
		except TweepError, e:
			self.process_exception(e)
		try:
			for tweet in tweets:
				self.tstatus = self.process_status(tweet)
				self.new_relationship, _ = TwitterRelationship.objects.get_or_create(influencer=self.influencer, action="TWEET", twitterStatus=self.tstatus, is_initial=self.is_initial)
				self.new_relationship.save()
				self.influencer.save()
		except TweepError, e:
			self.process_exception(e)
		return "Done"
		
	def process_status(self, status):
		self.hashtags = [x for x in status.entities['hashtags']]
		self.tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id = status.id, text=status.text.encode('utf-8'), favorite_count = status.favorite_count, retweet_count=status.retweet_count)
		self.tstatus.save()
		if not self.hashtags:
			return self.tstatus
		for hashtag in self.hashtags:
			self.h, _ = Hashtag.objects.get_or_create(name=hashtag['text'].lstrip('#').lower()) 
			self.h.save()
			self.tstatus.hashtags.add(self.h)
			self.tstatus.save()
		return self.tstatus


	def get_followers(self, screen_name=None, influencer=None, query_twitter=False, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name and is_initial==True and query_twitter==True:
			print "first if"
			try:
				self.twitter_followers = tweepy.Cursor(self.api.followers_ids).items()
			except TweepError, e:
				self.process_exception(e)
			try:
				for twitter_id in self.twitter_followers:
					tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
					tuser.save()
					self.socialprofile.add_follower(tuser, is_initial=self.is_initial)
					self.socialprofile.save()
			except TweepError, e:
				self.process_exception(e)
			return "Done"
		elif query_twitter == True:
			if not self.screen_name:
				try:
					self.twitter_ids = tweepy.Cursor(self.api.followers_ids).items()
				except TweepError, e:
					self.process_exception(e)
				return self.twitter_ids
			elif self.screen_name:
				try:
					self.twitter_ids = tweepy.Cursor(self.api.followers_ids, screen_name=self.screen_name).items()
				except TweepError, e:
					self.process_exception(e)
				return self.twitter_ids

		elif not self.screen_name and is_initial == False and query_twitter==False:
			self.db_followers = self.socialprofile.get_followers(socialProfile=self.socialprofile)
			self.db_followers_initial = self.socialprofile.get_initial_followers(socialProfile=self.socialprofile)
			
			if not self.db_followers and not self.db_followers_initial:
				return "No Database Followers"
			#if theres no database followers but there are initial followers (query happened once)
			elif not self.db_followers and self.db_followers_initial:
				print "only initial followers present"
				self.db_followers_ids = [x.twitterUser.twitter_id for x in self.db_followers_initial]
				try:
					self.twitter_followers = self.get_followers(query_twitter=True)
				except TweepError, e:
					self.process_exception(e)
				try:
					for i in self.twitter_followers:
						if i not in self.db_followers_ids:
							self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
							self.tuser.save()
							self.socialprofile.add_follower(self.tuser, is_initial=False)
							self.socialprofile.save()
						else:
							pass
				except TweepError, e:
					self.process_exception(e)

				return "Done"
				print([x for x in self.twitter_followers])
			#if there's both initial database followers and non_initial followers
			elif self.db_followers and self.db_followers_initial:
				self.db_followers_ids = [x.twitterUser.twitter_id for x in self.db_followers]
				self.db_initial_ids = [x.twitterUser.twitter_id for x in self.db_followers_initial]
				self.all_db_followers = self.db_followers_ids + self.db_initial_ids
				try:
					self.twitter_followers = self.get_followers(query_twitter=True)
				except TweepError, e:
					self.process_exception(e)
				try:
					for i in self.twitter_followers:
						if i not in self.all_db_followers:
							self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
							self.tuser.save()
							self.socialprofile.add_follower(self.tuser, is_initial=False)
							self.socialprofile.save()
						else:
							pass
				except TweepError, e:
					self.process_exception(e)
				return "Done"
			else:
				print "else jasd"
			print self.db_followers_initial
			self.db_followers_ids = [x.twitterUser.twitter_id for x in self.db_followers_initial]
		else:
			print "else"
			#####influencer followers fetch #####
			try:
				self.twitter_followers = tweepy.Cursor(self.api.followers_ids, screen_name=screen_name).items(5)
			except TweepError, e:
				self.process_exception(e)
			try:
				for twitter_id in self.twitter_followers:
					self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
					self.tuser.save()
					self.relationship, _ = TwitterRelationship.objects.get_or_create(influencer=self.influencer, twitterUser=self.tuser, action="FOLLOWER", is_initial=self.is_initial)
					self.influencer.save()
			except TweepError, e:
				self.process_exception(e)
			return "Done"

	def get_friends(self, screen_name=None, query_twitter=False, influencer=None, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name and is_initial==True:
			try:
				self.twitter_friends = tweepy.Cursor(self.api.followers_ids).items(5)
			except TweepError, e:
				self.process_exception(e)
			try:
				for twitter_id  in self.twitter_friends:
					tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
					tuser.save()
					self.socialprofile.add_friend(tuser, is_initial=self.is_initial)
					self.socialprofile.save()
			except TweepError, e:
				self.process_exception(e)
			return "Done"
		elif query_twitter == True:
			if not self.screen_name:
				return tweepy.Cursor(self.api.friends_ids).items()
			else:
				return tweepy.Cursor(self.api.friends_ids, screen_name=self.screen_name).items()
		elif not self.screen_name and is_initial==False:
			self.db_friends = self.socialprofile.get_friends()
			self.db_friends_ids = [x.twitterUser.twitter_id for x in self.db_friends]
			try:
				self.twitter_friends = self.get_friends(query_twitter=True)
			except TweepError, e:
				self.process_exception(e)
			try:
				for twitter_id in self.twitter_friends:
					if twitter_id not in self.db_friends_ids:
						self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
						self.tuser.save()
						self.socialprofile.add_friend(self.tuser, is_initial=False)
						self.socialprofile.save()
					else:
						pass
			except TweepyError, e:
				self.process_exception(e)
			return "Done"
		
		#####INFLUENCER FREINDS FETCH #######
		try:
			self.twitter_friends = tweepy.Cursor(self.api.followers_ids, screen_name=self.screen_name).items(5)
		except TweepError, e:
			self.process_exception(e)
		try:
			for twitter_id in self.twitter_friends:
				self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
				self.tuser.save()
				self.new_relationship = TwitterRelationship.objects.get_or_create(influencer=self.influencer, twitterUser=self.tuser, action="FRIEND", is_initial=self.is_initial)
				self.influencer.save()
		except TweepError, e:
			self.process_exception(e)
		return "Done"

	def get_favorites(self, screen_name=None, query_twitter=False, influencer=None, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name and is_initial == True:
			try:
				self.favorites = tweepy.Cursor(self.api.favorites).items()
			except TweepError, e:
				self.process_exception(e)
			try:
				for status in self.favorites:
					self.Tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id=status.id, text=status.text.encode('utf-8'), favorite_count=status.favorite_count, retweet_count=status.retweet_count)
					self.Tstatus.save()
					self.socialprofile.add_favorite(self.Tstatus, is_initial=self.is_initial) 
					self.socialprofile.save()
			except TweepError, e:
				self.process_exception(e)
			return "Done"
		elif query_twitter == True:
			if not self.screen_name:
				try:
					return tweepy.Cursor(self.api.favorites).items()
				except TweepError, e:
					self.process_exception(e)
			else:
				try:
					return tweepy.Cursor(self.api.favorites, screen_name=self.screen_name).items()
				except TweepError, e:
					self.process_exception(e)
		elif not self.screen_name and is_initial == False:
			self.db_favorites = self.socialprofile.get_favorites()
			self.db_favorites_ids = [x.twitterStatus.twitter_id for x in self.db_favorites]
			try:
				self.twitter_favorites = self.get_favorites(query_twitter=True)
			except TweepError, e:
				self.process_exception(e)
			try:
				for status in self.twitter_favorites:
					self.tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id=status.id, text=status.text.encode('utf-8'), favorite_count=status.favorite_count, retweet_count=status.retweet_count)
					self.tstatus.save()
					self.socialprofile.add_favorite(self.tstatus, is_initial=False)
					self.socialprofile.save()
			except TweepError, e:
				self.process_exception(e)
			return "Done"
		
		###Influencer Favorites Fetch ########
		try:
			self.favorites = tweepy.Cursor(self.api.favorites, screen_name=self.screen_name).items()
		except TweepError, e:
			self.process_exception(e)
		try:
			for status in self.favorites:
				self.Tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id=status.id, text=status.text.encode('utf-8'), favorite_count=status.favorite_count, retweet_count=status.retweet_count)
				self.Tstatus.save()
				self.new_relationship, _ = TwitterRelationship.objects.get_or_create(twitterStatus=self.Tstatus, influencer=self.influencer, action="FAVORITE", is_initial=self.is_initial)
				self.influencer.save()
		except TweepError, e:
			self.process_exception(e)
		return "Done"
	#followers, Friends, Tweets
	def get_everything(self, screen_name=None, influencer=None, query_twitter = False, is_initial=False):
		self.screen_name = screen_name
		if self.screen_name == None:
			self.get_followers(is_initial=self.is_initial, query_twitter=self.query_twitter)
			self.get_friends(is_initial=self.is_initial)
			self.get_favorites(is_initial=self.is_initial)
			self.get_tweets(is_initial=self.is_initial)
			self.get_tweet_count()
			self.follower_count = self.get_follower_count()
			self.friend_count = self.get_friends_count()
			self.socialprofile.followers_count=self.follower_count
			self.socialprofile.friend_count = self.friend_count
			self.socialprofile.save()
			return "Done"
		else:
			self.get_followers(is_initial=self.is_initial, screen_name=self.screen_name)
			self.get_friends(is_initial=self.is_initial, screen_name=self.screen_name)
			self.get_favorites(is_initial=self.is_initial, screen_name=self.screen_name)
			self.get_tweets(is_initial=self.is_initial, screen_name=self.screen_name)
			return "Done"

		



	def process_exception(self, e):
		if "Rate limit exceeded" in str(e):
			print 'rate limited, sleeping'
			time.sleep(900)
		else:
			print 'error'
		
	


class FetchSocialProfileInfo(Thread, TwitterGetFunctions):
	def __init__(self, is_initial=False, query_twitter=True, *args, **kwargs):
		self.queue = kwargs.pop('queue')
		self.socialprofile = kwargs.pop('socialprofile')
		self.action = kwargs.pop('action')
		self.is_initial = is_initial
		self.query_twitter = query_twitter
		print self.is_initial
		print "query twitter status {}".format(self.query_twitter)
		self.queue.put(self)
		TwitterGetFunctions.__init__(self, socialprofile=self.socialprofile,  *args, **kwargs)
		super(FetchSocialProfileInfo, self).__init__(*args, **kwargs)

	def run(self):
		if self.action == "Get_Everything":
			self.action = self.get_everything(is_initial=self.is_initial, query_twitter=self.query_twitter)
			if self.action == "Done":
				self.socialprofile.is_initial = False
				self.socialprofile.save()
			elif self.action == "Interrupted":
				self.socialprofile.save()
		elif self.action == "get_followers_and_friends_count":
			self.follower_count = self.get_follower_count()
			self.socialprofile.followers_count = self.follower_count
			self.socialprofile.save()
			self.friends_count = self.get_friends_count()
			self.socialprofile.friend_count = self.friends_count
			self.socialprofile.save()
		elif self.action =="Get_Tweet_Count":
			self.db_tweet_count = self.socialprofile.tweet_count
			print "Database Tweet count {}".format(self.db_tweet_count)
			self.tweet_count = self.get_tweet_count()
			if self.tweet_count != self.db_tweet_count:
				self.action = OnTweet(socialprofile=self.socialprofile)
			else:
				print "no new tweets"
			#self.socialprofile.tweet_count = self.tweet_count
			#self.socialprofile.save()
		elif self.action == "Get_Tweets":
			self.action = self.get_tweets(is_initial=self.is_initial)
		elif self.action == "Get_Followers":
			self.action = self.get_followers(is_initial=self.is_initial)
		elif self.action == "Get_Friends":
			self.action == self.get_friends(is_initial=self.is_initial)
		elif self.action == "Get_Favorites":
			self.action == self.get_favorites(is_initial=self.is_initial)

class FetchInfluencerInfo(Thread, TwitterGetFunctions):
	def __init__(self, is_initial=False, *args, **kwargs):
		self.is_initial = is_initial
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
			self.action = self.get_everything(influencer=self.influencer, is_initial=self.is_initial, screen_name=self.screen_name)
			if self.action == "Done":
				self.influencer.been_queried = True
				self.influencer.save()
			elif self.action == "Interrupted":
				self.influencer.save()
		elif self.action == "Get_Followers":
			self.action = self.get_followers(influencer=self.influencer, is_initial=self.is_initial, screen_name=self.screen_name)

		elif self.action == "Get_Tweets":
			self.action = self.get_tweets(influencer=self.influencer, is_initial=self.is_initial, screen_name=self.screen_name)

		elif self.action == "Get_Favorites":
			self.actioon = self.get_favorites(influencer=self.influencer, is_initial=self.is_initial, screen_name=self.screen_name)

		elif self.action == "Get_Friends":
			self.action = self.get_friends(influencer=self.influencer, is_initial=self.is_initial, screen_name=self.screen_name)

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

