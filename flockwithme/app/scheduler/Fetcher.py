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

class Fetch_Influencers_Followers(object):
	def __init__(self, lock=None, *args, **kwargs):
		self.influencer = kwargs.pop('influencer')
		self.screen_name = kwargs.pop('screen_name')
		self.queue = kwargs.pop('queue')
		self.lock = lock
		self.consumer_key = 'fYPmnEQtta3xXqS9CGhTwJf4M'
		self.consumer_secret = 'pVMlJRb47bYEPRrzRcGydYhcuWDwiaXPqgyDKahTtWf4tcu8A8'
		self.access_token = '258627515-fE5flw24GC8DPVWr5EE1nAVRWKwutkZOlH4L1Z0J'
		self.access_token_secret = '0fJsYMlf1KBtKCMP6RrLVxlAAuAjn34FEscVOSNSbjDO2'
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		self.queue.put(self)
		return super(Fetch_Influencers_Followers, self).__init__(*args, **kwargs)

	
		

	def fetch(self):
		self.twitter_followers = self.api.followers_ids(screen_name=self.screen_name)
		self.db_followers = [x.twitterUser.twitter_id for x in TwitterRelationship.objects.filter(influencer=self.influencer, action="FOLLOWER")]
		self.should_add = [x for x in self.twitter_followers if x not in self.db_followers]
		if len(self.should_add) > 1:
			for user in self.should_add:
				try:
					self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=tuser)
					self.tuser.save()
				except Exception, e:
					self.process_e = self.process_exception(e)
				try:
					self.add_relationship, _ = TwitterRelationship.objects.get_or_create(twitterUser=self.tuser, action="FOLLOWER")
				except Exception, e:
					self.process_e = self.process_exception(e)
				self.influencer.relationships.add(self.tuser)
				self.influencer.save()
			self.influencer.save()
		else:
			print 'Followers Fetched.'
			



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
		self.followers_to_be_added = []
		try:
			self.twitter_followers = set(tweepy.Cursor(api.followers_ids).items())
		except Exception, e:
			process_e = self.process_exception(e)
		
		for follower in self.twitter_followers:
			self.followers_to_be_added.append(follower)
		

		#get_my_following:

		self.friends_to_be_added = []
		
		try:
			self.following = set(tweepy.Cursor(api.friends_ids).items())
		except Exception, e:
			self.process_e = self.process_exception(e)
		
		for friend in self.following:
			try:
				self.friends_to_be_added.append(friend)
			except Exception, e:
				process_e = self.process_exception(e)
		

		########CLEANING TIME ###########
		#2. clean friends
		if len(self.friends_to_be_added) > 1:
			#compare the users friends on Twitter to his Friends in the database
			#add the ones that are present in his list of following on Twitter but aren't present in his list of following in our flock db.
			self.db_friends = [x.twitterUser.twitter_id for x in self.socialprofile.get_friends()]
			print 'database friends'
			print self.db_friends
			self.should_add = [x for x in self.friends_to_be_added if x not in self.db_friends]
			print 'should add'
			print self.should_add
			#if there's friends to add do this
			if len(self.should_add) > 1:
				for user in self.should_add:
					try:
						tuser, _ = TwitterUser.objects.get_or_create(twitter_id=user) 
					except Exception, e:
						self.process_e = self.process_exception(e)
					tuser.save()
					self.socialprofile.add_friend(tuser)
					self.socialprofile.save()
				if len(self.followers_to_be_added) > 1:
					self.db_followers = [x.twitterUser.twitter_id for x in self.socialprofile.get_followers()]
					self.should_add = [x for x in self.followers_to_be_added if x not in self.db_followers]
					if len(self.should_add) > 1:
						for user in self.should_add:
							try:
								self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=user)
							except Exception, e:
								self.process_e = self.process_exception(e)
							self.tuser.save()
							self.socialprofile.add_follower(self.tuser)
							self.socialprofile.save()
					else:
						self.socialprofile.job_status = "Account_Info_Fetched"
						self.socialprofile.save()
				else:
					self.socialprofile.job_status = 'Account_Info_Fetched'
					self.socialprofile.save()
			

			#otherwise do this
			else:
				if len(self.followers_to_be_added) > 1:
					self.db_followers = [x.twitterUser.twitter_id for x in self.socialprofile.get_followers()]
					self.should_add = [x for x in self.followers_to_be_added if x not in self.db_followers]
					if self.should_add > 1:
						for user in self.should_add:
							try:
								self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=user)
							except Exception, e:
								self.process_e = self.process_exception(e)

							self.tuser.save()
							self.socialprofile.add_follower(self.tuser)
						self.socialprofile.save()

		#3 Clean Followers
		elif len(self.followers_to_be_added) > 1:
			print len(self.followers_to_be_added)
			self.db_followers = [x.twitterUser.twitter_id for x in self.socialprofile.get_followers()]
			self.should_add = [x for x in self.followers_to_be_added if x not in self.db_followers]
			print 'followers we should add'
			print self.should_add
			if len(self.should_add) > 1:
				for user in should_add:
					tuser, _ = TwitterUser.objects.get_or_create(twitter_id = user)
					tuser.save()
					self.socialprofile.add_follower(tuser)
					self.socialprofile.save()
				self.socialprofile.save()
			else:
				self.socialprofile.job_status = "Account_Info_Fetched"
				self.socialprofile.save()
		else:
			self.socialprofile.job_status = "Account_Info_Fetched"
			self.socialprofile.save()



	def run(self):
		if self.action == "get_everything":
			action = self.get_everything()
			self.socialprofile.job_status = 'Account_Info_Fetched'
			self.socialprofile.save()
		else:
			print "use get everything"

	def process_exception(self, e):
		if "Rate limit exceeded" in str(e):
			print 'rate limited, sleeping'
			time.sleep(900)
		else:
			print 'error'
