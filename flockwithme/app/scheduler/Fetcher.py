import os
import sys
from optparse import OptionParser
from django.conf import settings
import time
import tweepy
from flockwithme.app.scheduler.models import OauthSet, Influencer, TwitterUser, TwitterRelationship, TwitterStatus, Hashtag
from flockwithme.core.profiles.models import SocialProfile
from threading import Thread




class Fetch_Social_Profile(object):
	def __init__(self, *args, **kwargs):
		self.access_token = kwargs.pop('token')
		self.access_token_secret = kwargs.pop('token_secret')
		self.consumer_key = '3Gsg8IIX95Wxq28pDEkA'
		self.consumer_secret = 'LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o'
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		return super(Fetch_Social_Profile, self).__init__(*args, **kwargs)

	def get_twitter_id(self):
		return self.api.me().id

	def get_follower_count(self):
		return self.api.me().followers_count

	def get_friend_count(self):
		return self.api.me().friends_count


class Fetch_Account_Info(Thread):
	def __init__(self, lock=None, *args, **kwargs):
		self.twitter_id = kwargs.pop('twitter_id')
		self.action = kwargs.pop('action')
		self.queue = kwargs.pop('queue')
		self.socialprofile = SocialProfile.objects.get(twitter_id=self.twitter_id)
		self.lock = lock
		self.queue.put(self)
		return super(Fetch_Account_Info, self).__init__(*args, **kwargs)

	def get_api(self):
		access_token = self.socialprofile.token
		access_token_secret = self.socialprofile.secret
		consumer_key = '3Gsg8IIX95Wxq28pDEkA'
		consumer_secret = "LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o"
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		return api
	def get_everything(self):
		api = self.get_api()
			
		#get_my_followers
		followers_to_be_added = []
		try:
			twitter_followers = set(tweepy.Cursor(api.followers_ids).items())
		except Exception, e:
			process_e = self.process_exception(e)
		
		for follower in twitter_followers:
			followers_to_be_added.append(follower)
		

		#get_my_following:

		friends_to_be_added = []
		
		try:
			following = set(tweepy.Cursor(api.friends_ids).items())
		except Exception, e:
			process_e = self.process_exception(e)
		
		for friend in following:
			friends_to_be_added.append(friend)
		#get my favorited tweets
		favorited_tweets_to_be_added = []
		try:
			favorites = tweepy.Cursor(api.favorites).items()
		except Exception, e:
			process_e = self.process_exception(e)
		
		for tweet in favorites:
			favorited_tweets.append(tweet)

		########CLEANING TIME ###########
		#1. Clean Favorites
		if len(favorited_tweets_to_be_added) > 1:
			#compare the tweets in my favorited tweets on twitter to my favorited tweets in the database
			#my_database_tweets
			database_favorites = set(self.socialprofile.get_favorites())
			should_add = database_favorites.difference(set(favorited_tweets_to_be_added))
			for tweet in should_add:
				tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id=tweet.id, text=tweet.text.encode('utf-8'), favorite_count=tweet.favorite_count, retweet_count=tweet.retweet_count)
				tstatus.save()
				self.socialprofile.add_favorite(tstatus)
				self.socialprofile.save()
		#2. clean friends
		elif len(friends_to_be_added) > 1:
			#compare the users friends on Twitter to his Friends in the database
			#add the ones that are present in his list of following on Twitter but aren't present in his list of following in our flock db.
			db_friends = set(self.socialprofile.get_friends())
			should_add = db_friends.difference(set(friends_to_be_added))
			for user in should_add:
				tuser, _ = TwitterUser.objects.get_or_create(twitter_id=user.id) 
				tuser.save()
				self.socialprofile.add_friend(tuser)
				self.socialprofile.save()
		#3 Clean Followers
		elif len(followers_to_be_added) > 1:
			db_followers = set(self.socialprofile.get_followers())
			should_add = db_followers.difference(set(followers_to_be_added))
			for user in should_add:
				tuser, _ = TwitterUser.objects.get_or_create(twitter_id = user.id)
				tuser.save()
				self.socialprofile.add_follower(tuser)
				self.socialprofile.save()


	def run(self):
		if self.action == "get_everything":
			action = self.get_everything()
		else:
			print "use get everything"

	def process_exception(e):
		if "Rate limit exceeded" in str(e):
			print 'rate limited, sleeping'
			time.sleep(900)
class Fetch_Twitter_Account(Thread):
	#
	def __init__(self, lock=None, *args, **kwargs):
		self.model = kwargs.pop('model')
		self.twitter_id = kwargs.pop('twitter_id')
		if self.model == 'SocialProfile':
			self.socialprofile = SocialProfile.objects.get(twitter_id=self.twitter_id)
		elif self.model == "Influencer":
			self.influencer = Influencer.objects.get(twitter_id=self.twitter_id)
		self.action = kwargs.pop('action')
		self.queue = kwargs.pop('queue')
		self.lock = lock
		return super(Fetch_Twitter_Account, self).__init__(*args, **kwargs)

	def get_api(self):
		try:
			self.auth_set = OauthSet.objects.filter(active=False, rate_limited=False)[0]
			print self.auth_set.c_key
			print self.auth_set.c_secret
			print self.auth_set.access_key
			print self.auth_set.key_secret
		except Exception, NoAuthSets:
			print 'No Auth Sets'
			print 'sleeping'
			time.sleep(200)
		self.auth = tweepy.OAuthHandler(str(self.auth_set.c_key), str(self.auth_set.c_secret))
		self.auth.set_access_token(str(self.auth_set.access_key), str(self.auth_set.key_secret))
		self.api = tweepy.API(self.auth)
		return self.api
		
	def get_follower_count(self):
		api = self.get_api()
		return api.get_user(user_id=self.twitter_id).followers_count
		

	def get_friend_count(self):
		api = self.get_api()
		print dir(api)
		return api.get_user(user_id=self.twitter_id).friends_count

	def get_twitter_id(self):
		api = self.get_api()
		return api.get_user(user_id=self.twitter_id).id

	def get_follower_ids(self, twitter_id=None):
		api = self.get_api()
		return set(api.followers_ids(user_id=self.twitter_id))

	def get_friend_ids(self, twitter_id=None):
		api = self.get_api()
		return set(api.friends_ids(user_id=twitter_id))

	def get_favorited_tweets(self, twitter_id=None):
		api = self.get_api()
		statuses = []
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
		print api.me()
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
		elif self.action == "get_friend_count":
			action = self.get_follower_count()
		elif self.action == 'get_everything':
			if self.twitter_id == None:
				t_id = self.get_twitter_id()
			else:
				t_id = self.twitter_id
			friend_count = self.get_friend_count()
			follower_count = self.get_follower_count()
			follower_ids = self.get_follower_ids()
			friend_ids = self.get_friend_ids()
			if self.model == 'Influencer':
				influencer_instance = Influencer.objects.get(twitter_id=self.twitter_id)
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

			







	







