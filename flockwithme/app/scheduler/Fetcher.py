import os
import sys
from optparse import OptionParser
from django.conf import settings
import time
import tweepy
from flockwithme.app.scheduler.models import OauthSet, Influencer, TwitterUser, TwitterRelationship, TwitterStatus, Hashtag
from flockwithme.core.profiles.models import SocialProfile
from threading import Thread




class Fetch_Twitter_Account(Thread):
	def __init__(self, lock=None, *args, **kwargs):
		self.action = kwargs.pop('action')
		self.lock = lock
		try:
			self.queue = kwargs.pop('queue')
		except Exception, NoQueue:
			pass
		try:
			self.model = kwargs.pop('model')
		except Exception, NoModel:
			pass
		try:
			self.screen_name = kwargs.pop('screen_name')
		except Exception, no_screename:
			pass

		try:
			self.twitter_id = kwargs.pop('twitter_id')
		except Exception, NoTId:
			self.twitter_id = None
		if self.twitter_id != None:
			self.socialprofile = SocialProfile.objects.get(twitter_id=self.twitter_id)
		else:
			self.socialprofile = SocialProfile.objects.get(handle=self.screen_name)
		try:
			self.auth_set = OauthSet.objects.filter(rate_limited=False, active=False)[0]
		except Exception, NoAuthSet:
			self.auth_set = None
			process_e = self.process_exception(NoAuthSet)
			
			
		self.queue.put(self)

		return super(Fetch_Twitter_Account, self).__init__(*args, **kwargs)

	def get_api(self):
		auth_set = self.auth_set
		try:
			auth = tweepy.OAuthHandler(auth_set.c_key, auth_set.c_secret)
		except Exception, NoneType:
			for i in OauthSet.objects.filter(rate_limited=True):
				i.rate_limited = False
				i.save()
		try:
			auth.set_access_token(auth_set.access_key, auth_set.key_secret)
		except Exception, e:
			process_e = self.process_exception(e)

		try:
			api = tweepy.API(auth)
		except Exception, e:
			process_e = self.process_exception(e)
		return api
	def get_follower_count(self, twitter_id=None):
		api = self.get_api()
		if twitter_id == None:
			return api.get_user(screen_name=self.screen_name).followers_count
		else:
			return api.get_user(user_id=twitter_id).followers_count

	def get_friend_count(self, twitter_id=None):
		api = self.get_api()
		if twitter_id == None:
			return api.get_user(screen_name=self.screen_name).friends_count
		else:
			return api.get_user(user_id=twitter_id).friends_count

	def get_twitter_id(self):
		api = self.get_api()
		return api.get_user(screen_name=self.screen_name).id

	def get_follower_ids(self, twitter_id=None):
		api = self.get_api()
		if twitter_id == None:
			return set(api.followers_ids(screen_name=self.screen_name))
		else:
			return set(api.followers_ids(user_id=twitter_id))

	def get_friend_ids(self, twitter_id=None):
		api = self.get_api()
		if twitter_id == None:
			return set(api.friends_ids(screen_name=self.screen_name))
		else:
			return set(api.friends_ids(user_id=twitter_id))

	def get_favorited_tweets(self, twitter_id=None):
		api = self.get_api()
		statuses = []
		if twitter_id == None:
			try:
				for i in tweepy.Cursor(api.favorites, user_id=self.screen_name).items():
					statuses.append(i)
			except Exception, e:
				process_e = self.process_exception(e)
	
		else:
			try:
				for i in tweepy.Cursor(api.favorites, user_id=self.twitter_id).items():
					statuses.append(i)
			except Exception, e:
				process_e = self.process_exception(e)
		return statuses

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
		user.screen_name = status.user.screen_name.encode('utf-8')
		user.favorites_count = status.user.favourites_count
		user.followers_count = status.user.followers_count
		user.friends_count = status.user.friends_count
		user.verified = status.user.verified
		user.location = status.user.location.encode('utf-8')
		user.statuses_count = status.user.statuses_count
		user.twitter_id = status.user.id
		user.save()

		mstatus = TwitterStatus()
		mstatus.twitter_id = status.id
		mstatus.text = status.text.encode('utf-8')
		mstatus.twitter_user = user
		mstatus.favorite_count = status.favorite_count
		mstatus.retweet_count = status.retweet_count
		mstatus.save()
		self.socialprofile.add_favorite(mstatus)
		for d in status.entities['hashtags']:
			hashtag, _ = Hashtag.objects.get_or_create(name=d['text'].lstrip('#').lower())
			mstatus.hashtags.add(hashtag)
		mstatus.save()
		return mstatus

	def check_ratio(self):
		api = self.get_api()
		friend_count = api.get_user(user_id=self.twitter_id).friends_count
		follower_count = api.get_user(user_id=self.twitter_id).followers_count
		self.socialprofile.followers_count = follower_count
		self.socialprofile.friend_count = friend_count
		if friend_count > follower_count:
			self.socialprofile.job_status = "Ratio_Bad"
		else:
			self.socialprofile.job_status = "Ratio_Good"
		self.socialprofile.save()


	def run(self):
		if self.action == 'get_twitter_id':
			self.get_twitter_id()
		elif self.action == 'get_everything':
			if self.twitter_id == None:
				t_id = self.get_twitter_id()
			else:
				t_id = self.twitter_id
			friend_count = self.get_friend_count(twitter_id=self.twitter_id)
			follower_count = self.get_follower_count(twitter_id=self.twitter_id)
			follower_ids = self.get_follower_ids(twitter_id=self.twitter_id)
			friend_ids = self.get_friend_ids(twitter_id=self.twitter_id)
			if self.model == 'Influencer':
				influencer_instance = Influencer.objects.get(screen_name=self.screen_name)
				influencer_instance.twitter_id = t_id
				influencer_instance.friend_count = friend_count
				influencer_instance.followers_count = follower_count
				for i in follower_ids:
					tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
					tuser.save()
					new_follower = TwitterRelationship.objects.create(twitterUser=tuser, action='FOLLOWER')
					influencer_instance.relationships.add(new_follower)
				for i in friend_ids:
					tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
					tuser.save()
					new_friend = TwitterRelationship.objects.create(twitterUser=tuser, action="FRIEND")
					influencer_instance.relationships.add(new_friend)
				influencer_instance.save()
			elif self.model == "SocialProfile":
				follower_ids = self.get_follower_ids()
				friend_ids = self.get_friend_ids()
				favorited_tweets = self.get_favorited_tweets()
				for i in follower_ids:
					try:
						tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
					except Exception, e:
						process_e = self.process_exception(e)
					tuser.save()
					self.socialprofile.add_follower(tuser)
				for i in friend_ids:
					try:
						tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
					except Exception, e:
						process_e = self.process_exception(e)
					tuser.save()
					self.socialprofile.add_friend(tuser)
				for status in favorited_tweets:
					try:
						mstatus = self.process_status(status)
					except Exception, e:
						process_e = self.process_exception(e)
					
					self.socialprofile.add_favorite(mstatus)
				self.socialprofile.save()
					


		elif self.action == 'get_friends_and_followers':
			follower_ids = self.get_follower_ids()
			friend_ids = self.get_friend_ids()
			if self.model == 'SocialProfile' and self.twitter_id != None:
				for i in follower_ids:
					tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
					tuser.save()
					self.socialprofile.add_follower(tuser)
				for i in friend_ids:
					tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
					tuser.save()
					self.socialprofile.add_friend(tuser)
				self.socialprofile.job_status = 'Account_Info_Fetched'
				self.socialprofile.save()

		elif self.action == 'GET_FAVORITES':
			fav_tweets = self.get_favorited_tweets()
			for tweet in fav_tweets:
				try:
					cleaned_status = self.process_status(tweet)
				except Exception, e:
					process_e = self.process_exception(e)
			self.socialprofile.job_status = 'FAVORITES_FETCHED'

		elif self.action == "Check_Ratio":
			action = self.check_ratio()
			return True



	def process_exception(self, e):
		if "Rate limit exceeded" in str(e):
			print e
			self.auth_set.rate_limited = True
			self.auth_set.save()
			try:
				self.auth_set = OauthSet.objects.filter(active=False, rate_limited=False)
			except Exception, NoAuthTokens:
				time.sleep(9)
				for i in OauthSet.objects.filter(active=True, rate_limited=True):
					i.rate_limited = False
					i.active = False
					i.save()
				self.auth_set = OauthSet.objects.filter(active=False, rate_limited=False)
			return super(Fetch_Twitter_Account, self).__init__()
		else:
			print e

			







	







