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
		access_token = self.socialprofile.token
		access_token_secret = self.socialprofile.secret
		consumer_key = '3Gsg8IIX95Wxq28pDEkA'
		consumer_secret = 'LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o'
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		return api

	def follow(self):
		api = self.get_api()
		following = self.get_friends()
		followers = self.get_followers()
		following_ids = set(x.twitterUser.twitter_id for x in following)
		author_ids = [x.twitter_user.twitter_id for x in self.get_tweets()]
		influencers = self.profile.influencers.all()
		authors_and_followers = []
		for i in influencers:
			twitter_ids = self.get_followers_of_influencer(i.id)
			for i in twitter_ids:
				authors_and_followers.append(i)
		for i in author_ids:
			authors_and_followers.append(i)

		to_follow_set = set(authors_and_followers)
		should_follow = to_follow_set.difference(following_ids)
		#################NOW TIME FOR THE FOLLOWING BITCHES ##############
		followers_count = api.me().followers_count
		friends_count = api.me().friends_count
		followed = []
		while followers_count > friends_count:
			for i in should_follow:
				try:
					api.create_friendship(user_id=i)
				except Exception, e:
					process_e = self.process_exception(e)
				followed.append(i)
		for i in followed:
			tuser, _ = TwitterUser.objects.get_or_create(twitter_id=i)
			tuser.save()
			self.socialprofile.add_friend(tuser)
		self.socialprofile.job_status = 'Just_Followed'
		self.socialprofile.friend_count = api.me().friends_count
		self.socialprofile.follower_count = api.me().followers_count
		self.socialprofile.save()









	def unfollow(self):
		api = self.get_api()
		user = self.socialprofile.twitter_id
		following = self.get_friends()
		followers = self.get_followers()
		following_ids = [x.twitterUser.twitter_id for x in following)
		friend_ids = [x.twitterUser.twitter_id for x in followers]
		non_followers = [x for x in friend_ids if x not in following_ids]
		if non_followers > 1:
			try:
				for twitter_id in non_followers:
					try:
						self.api.destroy_friendship(user_id=twitter_id)
					except Exception, e:
						self.process_e = self.process_exception(e)
					self.tuser = TwitterUser.objects.get(twitter_id=twitter_id)
				#add the twitter user to the social profiles unfollowed lists
					self.socialprofile.add_unfriend(self.tuser)
				#removie the twitter user from the socialprofiles list of following
					self.socialprofile.delete_friend(self.tuser)
				self.socialprofile.save()
			except Exception, e:
				process_e = self.process_exception(e)
		else:
			#query twitter for ids of people who are following me
			try:
				self.followers = api.followers_ids())
			except Exception, e:
				proccess_e = self.process_exception(e)
			#query twitter for ids of people who are following me.
			try:
				self.friends = api.friends_ids())
			except Exception, e:
				process_e = self.process_exception(e)
			time.sleep(20)

			non_followers = [x for x in self.friends if x not in self.followers]
			if non_followers:
				for user in non_followers:
					try:
						self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=user)
						self.tuser.save()
					except Exception, e:
						process_e = self.process_exception(e) 

					try:
						api.destroy_friendship(user)
						self.socialprofile.add_unfriend(self.tuser)
					except Exception, e:
						process_e = self.process_exception(e)
				return 'clean'
			else:
				return 'no_unfollowers'


	def favorite(self):
		api = self.get_api()
		tweet_ids = set(x.twitter_id for x in self.get_tweets())
		favorited_tweets = set(x.twitterStatus.twitter_id for x in self.socialprofile.get_favorites())
		for i in tweet_ids:
			if i not in favorited_tweets:
				try:
					api.create_favorite(i)
				except Exception, e:
					process_e = self.process_exception(e)
				self.socialprofile.add_favorite(i)
		self.socialprofile.job_status="Just_Favorited"
		self.socialprofile.save()


	def direct_message(self):
		pass

	def get_tweets(self):
		hashtags = self.profile.hashtags.all()
		already_favorited = self.socialprofile.get_favorites()
		tweets = []
		for i in hashtags:
			return [x for x in TwitterStatus.objects.filter(hashtags=i) if x not in already_favorited]


	def get_followers_of_influencer(self, influencer_id):
		influencer = Influencer.objects.get(pk=influencer_id)
		return [x.twitterUser.twitter_id for x in influencer.relationships.filter(action="FOLLOWER")]

	def get_friends(self):
		return set(self.socialprofile.get_friends())

	def get_followers(self):
		return set(self.socialprofile.get_followers())


	def get_unfollowed(self):
		return self.socialprofile.get_unfriended()

	def clean_account(self):
		friend_count = self.socialprofile.friend_count
		followers_count = self.socialprofile.followers_count
		if friend_count > followers_count:
			action = self.unfollow()
			if action == 'unfollowed':
				return 'cleaned'
			
			elif action == "no_unfollowers":
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
			elif action == 'clean':
				self.socialprofile.job_status = 'Ratio_Good'
				self.socialprofile.save()
			elif action == 'cleaned':
				self.socialprofile.job_status = "Just_Cleaned"
				self.socialprofile.save()
			else:
				self.socialprofile.job_status = "Ratio_Bad"
				self.socialprofile.save()
		
		elif self.action == 'Follow':
			action = self.follow()
			self.socialprofile.job_status = "Just_Followed"
			self.socialprofile.save()
		elif self.action == 'FAVORITE':
			action = self.favorite()
			self.socialprofile.job_status = "Just_Favorited"
			self.socialprofile.save()
		

	def process_exception(self, e):
		print e
		
		
		


		
		



