import os
import sys
import time
import tweepy
import math
import random
from threading import Thread
from flockwithme.app.scheduler.models import TwitterStatus, TwitterUser, Influencer
from flockwithme.core.profiles.models import Profile


class AutoPilot(Thread):
	def __init__(self, lock=None, action=None, *args, **kwargs):
		self.queue = kwargs.pop('queue')
		self.socialprofile = kwargs.pop('account')
		self.action = action
		self.profile = Profile.objects.get(accounts=self.socialprofile)
		self.time = time.time()
		self.lock = lock
		self.queue.put(self)
		return super(AutoPilot, self).__init__(*args, **kwargs)
		

	def get_api(self):
		self.access_token = self.socialprofile.token
		self.access_token_secret = self.socialprofile.secret
		self.consumer_key = '3Gsg8IIX95Wxq28pDEkA'
		self.consumer_secret = 'LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o'
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		return self.api

	def sleep_action(self):
		return time.sleep(random.randint(0,100))
	def follow(self):
		self.api = self.get_api()
		self.following = self.get_friends()
		self.followers = self.get_followers()
		self.following_ids = [x.twitterUser.twitter_id for x in self.following]
		self.author_ids = self.get_author_ids()
		print self.author_ids
		return
		self.influencers = self.profile.influencers.all()
		self.authors_and_followers = []
		if len(self.influencers) > 0:
			try:
				for i in self.influencers:
					self.twitter_ids = self.get_followers_of_influencer(i.id)
			except Exception, e:
				self.process_e = self.process_exception(e)
			if len(self.twitter_ids) > 0:
				try:
					for i in self.twitter_ids:
						self.authors_and_followers.append(i)
				except Exception, e:
					self.process_e = self.process_exception(e)
		
			else:
				print 'no influencers'
		else:
			print "no influencers"
		
		if len(self.author_ids) > 0:
			try:
				for i in self.author_ids:
					self.authors_and_followers.append(i)
			except Exception, e:
				self.process_e = self.process_exception(e)
		else:
			print "no author_ids"

		self.should_follow = [x for x in self.authors_and_followers if x not in self.following_ids]
		print self.should_follow
		#################NOW TIME FOR THE FOLLOWING BITCHES ##############
		self.followers_count = api.me().followers_count
		self.friends_count = api.me().friends_count
		self.followed = []
		self.follow_limit = len(self.followers_count) - len(self.friends_count)
		if self.follow_limit >= 1000:
			self.follow_limit = 800
		print self.follow_limit
		self.num_followed = 0
		#if there's users to follow
		if len(self.should_follow) > 0: 
			while self.num_followed < self.follow_limit:
				for i in self.should_follow:
					try:
						self.api.create_friendship(user_id=i)
					except Exception, e:
						process_e = self.process_exception(e)
					self.followed.append(i)
					self.sleep_action()
			#if users were followed
			if len(self.followed) > 0:
				for i in self.followed:
					try:
						self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
					except Exception, e:
						self.process_e = self.process_exception(e)
					self.tuser.save()
					self.socialprofile.add_friend(self.tuser)
			else:
				self.socialprofile.job_status = "No_Users_To_Follow"
				self.socialprofile.save()
		#if there are no users to follow
		else:
			self.socialprofile.job_status = "No_Users_To_Follow"
			self.socialprofile.save()
		self.socialprofile.job_status = 'Just_Followed'
		self.socialprofile.friend_count = api.me().friends_count
		self.socialprofile.follower_count = api.me().followers_count
		self.socialprofile.save()









	def unfollow(self):
		self.api = self.get_api()
		self.user = self.socialprofile.twitter_id
		self.friends = self.get_friends()
		print "following"
		print self.friends
		self.followers = self.get_followers()
		print "followers"
		print self.followers
		#People following the user
		self.followers_ids = [x.twitterUser.twitter_id for x in self.followers]
		#people the user is following
		self.friend_ids = [x.twitterUser.twitter_id for x in self.friends]
		self.non_followers = [x for x in self.friend_ids if x not in self.followers_ids]
		print "non followers"
		self.unfollowed = []
		if self.non_followers > 1:
			print "true"
			for twitter_id in self.non_followers:
				try:
					self.api.destroy_friendship(twitter_id)
				except Exception, e:
					self.process_e = self.process_exception(e)
				self.unfollowed.append(twitter_id)
		
			if len(self.unfollowed) > 0:
				for twitter_id in self.unfollowed:
					try:
						self.tuser = TwitterUser.objects.get(twitter_id=twitter_id)
					except Exception, e:
						self.process_e = self.process_exception(e)
				#add the twitter user to the social profiles unfollowed lists
					try:
						self.socialprofile.add_unfriend(self.tuser)
					except Exception, e:
						self.process_e = self.process_exception(e)
					self.socialprofile.save()
				#removie the twitter user from the socialprofiles list of following
					#get the twitter relationship object using the twitter id and action arguments
					try:
						self.socialprofile.relationships.remove(self.tuser, "FRIEND")
					except Exception, e:
						self.process_e = self.process_exception(e)
					self.socialprofile.save()
				
				self.socialprofile.save()

				#return unfollowed
				return "unfollowed"
			else:
				print "No one was unfollowed"
		#if the user has no non-followers
		else:
			#query twitter for ids of people who are following them
			try:
				self.followers = api.followers_ids()
			except Exception, e:
				self.proccess_e = self.process_exception(e)
			#query twitter for ids of people they are following.
			try:
				self.friends = api.friends_ids()
			except Exception, e:
				self.process_e = self.process_exception(e)
			#sleep for 20 seconds
			self.time.sleep(20)

			self.non_followers = [x for x in self.friends if x not in self.followers]
			if self.non_followers:
				for user in self.non_followers:
					try:
						self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=user)
						self.tuser.save()
					except Exception, e:
						process_e = self.process_exception(e) 

					try:
						self.api.destroy_friendship(user)
						self.socialprofile.add_unfriend(self.tuser)
						#sleep for a random amount of time after unfollowing
						self.sleep_action()
					except Exception, e:
						self.process_e = self.process_exception(e)
				return 'clean'
			#if no non_followers
			else:
				return 'no_unfollowers'


	def favorite(self):
		self.api = self.get_api()
		self.tweet_ids = set(x.twitter_id for x in self.get_tweets())
		self.favorited_tweets = set(x.twitterStatus.twitter_id for x in self.socialprofile.get_favorites())
		for i in self.tweet_ids:
			if i not in self.favorited_tweets:
				try:
					self.api.create_favorite(i)
				except Exception, e:
					self.process_e = self.process_exception(e)
				self.socialprofile.add_favorite(i)
		self.socialprofile.job_status="Just_Favorited"
		self.socialprofile.save()


	def direct_message(self):
		pass

	def get_tweets(self):
		self.hashtags = self.profile.hashtags.all()
		self.already_favorited = [x.twitter_status.twitter_id for x in self.socialprofile.get_favorites()]
		self.tweets = []
		for i in self.hashtags:
			self.statusses = [x for x in TwitterStatus.objects.filter(hashtags=i) if x.twitter_id not in self.already_favorited]
			self.tweets.append(y for y in self.statusses)
		return self.tweets

	def get_author_ids(self):
		self.hashtags = self.profile.hashtags.all()
		self.already_followed = [x.twitterUser.twitter_id for x in self.socialprofile.get_friends()]   
		self.author_ids = []
		for i in self.hashtags:
			self.author_id = [x.twitter_user.twitter_id for x in TwitterStatus.objects.filter(hashtags=i) if x not in self.already_followed]
			self.author_ids.append(x for x in self.author_id)
		return self.author_ids

	def get_followers_of_influencer(self, influencer_id):
		self.influencer = Influencer.objects.get(pk=influencer_id)
		return [x.twitterUser.twitter_id for x in self.influencer.relationships.filter(action="FOLLOWER")]

	def get_friends(self):
		return self.socialprofile.get_friends()

	def get_followers(self):
		return self.socialprofile.get_followers()


	def get_unfollowed(self):
		return self.socialprofile.get_unfriended()

	def clean_account(self):
		self.friend_count = self.socialprofile.friend_count
		self.followers_count = self.socialprofile.followers_count
		if self.friend_count > self.followers_count:
			self.action = self.unfollow()
			print self.action
			if self.action == 'unfollowed':
				self.socialprofile.friend_count = self.get_api().me().friends_count
				self.socialprofile.followers_count = self.get_api().me().followers_count
				self.friend_ids = [x.twitterUser.twitter_id for x in self.socialprofile.get_friends()]
				self.unfriended = [x.twitterUser.twitter_id for x in self.socialprofile.get_unfriended()]
				self.should_remove = [x for x in self.friend_ids if x in self.unfriended]
				if self.should_remove:
					for i in self.should_remove:
						self.tuser = TwitterUser.objects.get(twitter_id=i)
						self.socialprofile.relationships.remove(self.tuser, "FRIEND")
					self.socialprofile.save()
				return 'cleaned'
			
			elif self.action == "no_unfollowers":
				try:
					self.followers_count = self.get_api().me().followers_count
					self.friends_count = self.get_api().me().friends_count
				except Exception, e:
					self.process_e = self.process_exception(e)
				try:
					if self.followers_count and self.friends_count:
						if self.followers_count < self.friends_count:
							return "Ratio_Dirty_No_Unfollowers"
						else:
							return "Ratio_Clean_No_Unfollowers"
				except Exception, e:
					self.process_e = self.process_exception(e)
			else:
				return 'not_clean'
		return 'clean'



	def run(self):
		if self.action == 'clean_account':
			self.action = self.clean_account()
			if self.action == "Ratio_Dirty_No_Unfollowers":
				self.socialprofile.job_status = "Ratio_Dirty_No_Unfollowers"
				self.socialprofile.save()
			elif self.action == "Ratio_Clean_No_Unfollowers":
				self.socialprofile.job_status = "Ratio_Good"
				self.socialprofile.save()
			elif self.action == 'clean':
				self.socialprofile.job_status = 'Ratio_Good'
				self.socialprofile.save()
			elif self.action == 'cleaned':
				self.socialprofile.job_status = "Just_Cleaned"
				self.socialprofile.save()
			else:
				self.socialprofile.job_status = "Ratio_Bad"
				self.socialprofile.save()
		
		elif self.action == 'Follow':
			self.action = self.follow()
			self.socialprofile.job_status = "Just_Followed"
			self.socialprofile.save()
		elif self.action == 'FAVORITE':
			self.action = self.favorite()
			self.socialprofile.job_status = "Just_Favorited"
			self.socialprofile.save()
		

	def process_exception(self, e):
		if "Rate limit exceeded" in str(e):
			print e
			print "sleeping"
			self.time.sleep(900)	
		else:
			print e
		
		
		


		
		



