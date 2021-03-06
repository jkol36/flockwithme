import os
import sys
import time
import math
import random
from threading import Thread

import tweepy
from tweepy.error import TweepError


from flockwithme.app.scheduler.models import TwitterStatus, TwitterUser, Influencer, ApiStatus
from flockwithme.core.profiles.models import Profile




class AutoPilot(object):
	def __init__(self, socialprofile, queue, jobs, action=None, *args, **kwargs):
		self.queue = queue
		self.socialprofile = socialprofile
		self.jobs = jobs
		self.action = action
		self.profile = Profile.objects.get(accounts=self.socialprofile)
		self.time = time.time()
		self.queue.put(self)
		self.run()
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
		return time.sleep(random.randint(0,10))
	def follow(self):
		self.api = self.get_api()
		#self.following = self.get_friends()
		#self.followers = self.get_followers()
		#self.following_ids = [x.twitterUser.twitter_id for x in self.following]
		self.author_ids = self.get_author_ids()
		self.influencers = self.profile.influencers.all()
		self.twitter_ids = [x for x in self.author_ids]
		for i in self.influencers:
			twitter_ids.append(i)
		return self.twitter_ids
		
		#self.should_follow = [x for x in self.authors_and_followers if x not in self.following_ids]
		#print self.should_follow
		#################NOW TIME FOR THE FOLLOWING BITCHES ##############
		self.followers_count = self.get_api().me().followers_count
		self.friends_count = self.get_api().me().friends_count
		self.followed = []
		self.follow_limit = self.followers_count - self.friends_count
		if self.follow_limit >= 1000:
			self.follow_limit = 800
		print self.follow_limit
		self.num_followed = 0
		#if there's users to follow
		
		while self.num_followed < self.follow_limit:
			for i in self.authors_and_followers:
				try:
					self.api.create_friendship(i)
				except Exception, e:
					process_e = self.process_exception(e)
			
				try:
					self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
				except Exception, e:
					self.process_e = self.process_exception(e)
				self.tuser.save()
				self.socialprofile.add_friend(self.tuser)
				self.num_followed += 1
				self.followed.append(i)
				self.sleep_action()
		#if users were followed
		if len(self.followed) > 0:
			self.socialprofile.job_status = 'Just_Followed'
			self.socialprofile.friend_count = api.me().friends_count
			self.socialprofile.follower_count = api.me().followers_count
			self.socialprofile.save()
		else:
			self.socialprofile.job_status = "No_Users_To_Follow"
			self.socialprofile.save()
		
		









	def unfollow(self):
		self.api = self.get_api()
		self.user = self.socialprofile.twitter_id
		self.friends = self.get_friends()
		self.followers = self.get_followers()
		#People following the user
		self.followers_ids = [x.twitterUser.twitter_id for x in self.followers]
		#people the user is following
		self.friend_ids = [x.twitterUser.twitter_id for x in self.friends]
		self.non_followers = [x for x in self.friend_ids if x not in self.followers_ids]
		self.unfollowed = []

		if not self.non_followers > 1:
			try:
				self.followers = self.api.followers_ids()
			except TweepError as e:
				self.handle_e = self.process_exception(e)
			
			try:
				self.friends = self.api.friends_ids()
			except TweepError as e:
				self.handle_e = self.process_exception(e)

			self.non_followers = [x for x in self.friends if x not in self.followers]

			if not self.non_followers:
				return "no_unfollowers"

			for twitter_id in self.non_followers:
				try:
					self.api.destroy_friendship(twitter_id)
				except TweepError as e:
					self.handle_e = self.process_exception(e)
				self.unfollowed.append(twitter_id)
			
			if not len(self.unfollowed) > 0:
				print "No one was unfollowed"

			for twitter_id in self.unfollowed:
				self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
				self.tuser.save()
				self.socialprofile.add_unfriend(self.tuser)
				self.socialprofile.relationships.remove(self.tuser, 'FRIEND')
			self.socialprofile.save()


		for twitter_id in self.non_followers:
			try:
				self.api.destroy_friendship(twitter_id)
			except TweepError as e:
				self.handle_e = self.process_exception(e)
			self.unfollowed.append(twitter_id)
		for twitter_id in self.unfollowed:
			self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
			self.tuser.save()
			self.socialprofile.add_unfriend(self.tuser)
			self.socialprofile.relationships.remove(self.tuser, "FRIEND")
		self.socialprofile.save()


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
		print dir(self.socialprofile)

	def get_tweets(self):
		self.hashtags = self.profile.hashtags.all()
		self.already_favorited = [x.twitter_status.twitter_id for x in self.socialprofile.get_favorites()]
		self.tweets = []
		for i in self.hashtags:
			self.statusses = [x for x in TwitterStatus.objects.filter(hashtags=i)[:1000] if x.twitter_id not in self.already_favorited]
			self.tweets.append(y for y in self.statusses)
		return self.tweets

	def get_author_ids(self):
		self.hashtags = self.profile.hashtags.all()
		self.friends = self.get_friends()
		print self.hashtags
		self.author_ids = []
		for i in self.hashtags:
			self.author_id = [x.twitter_user.twitter_id for x in TwitterStatus.objects.filter(hashtags=i).order_by('created_at')[:100] if x not in self.friends]
			self.author_ids.append(self.author_id)
		return self.author_ids

	def get_followers_of_influencer(self, influencer_id):
		self.influencer = Influencer.objects.get(pk=influencer_id)
		self.friends = self.get_friends()
		return [x.twitterUser.twitter_id for x in self.influencer.relationships.filter(action="FOLLOWER")[:900] if x not in self.friends]

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


	def process_exception(e):
		print e

	def run(self):
		follow = False
		favorite = False
		DM = False
		print self.follow()

		
		
		


		
		



