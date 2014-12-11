# -*- coding: utf-8 -*-
from threading import Thread
from django.conf import settings
from flockwithme.app.scheduler.models import OauthSet, TwitterUser
from flockwithme.core.profiles.models import Profile
import tweepy
from time import sleep
import random
import logging
logger = logging.getLogger(__name__)

class AccountFetch(Thread):
	def __init__(self, *args, **kwargs):
		self.jobs = kwargs.pop('jobs')
		self.account = kwargs.pop("account")
		self.queue = kwargs.pop("queue")
		self.api = self.get_api()
		return super(AccountFetch, self).__init__(*args, **kwargs)
		self.daemon = True
		self.queue.put(self)
	#
	def create_twitter_user(self, twitter_id, screen_name, friends_count, followers_count, location):
		new_twitter_user = TwitterUser.objects.create(twitter_id=twitter_id, screen_name = screen_name, friends_count=friends_count, followers_count=followers_count)
		new_twitter_user.save()
		return new_twitter_user

	def get_twitter_user(self, twitter_id):
		twitter_user_instance = TwitterUser.objects.get(twitter_id=twitter_id)
	
	#On rate limited the token_set will be suspended for 15 minutes	
	def change_status_to_rate_limited(self, auth_set_id):
		rate_limited = OauthSet.objects.get(id=auth_set_id)
		rate_limited.rate_limited = True
		rate_limited.save()
 

	def get_followers(self, auth):
		api = self.get_api(auth)
		follower_ids = tweepy.Cursor(api.followers_ids()).items()
		return follower_ids
	
	def FetchAccount(self, job):
		api = self.get_api()['auth']
		auth_set_instance = self.get_api()['auth_set']
		profile_instance = job.socialprofile
		#api call
		try:
			twitter_followers = tweepy.Cursor(followers_ids, screen_name=profile_instance).items()
		except Exception RateLimited:
			self.change_status_to_rate_limited(auth_set_instance)
			self.get_api()

		while True:
			try:
				current_twitter_ids = [x.twitter_id for x in TwitterUser.objects.all()]
				#Query Twitter if the ID is not present in our database
				should_query = [x for x in twitter_followers if x not in current_twitter_ids]
				#Query our database to fetch the twitter profile if the id is present in our database
				remaining = [x for x in twitter_followers if x in current_twitter_ids]
				if should_query:
					for twitter_id in should_query:
						#api call
						profile = api.get_user(user_id=twitter_id)
						try:
							new_twitter_user = self.create_twitter_user(twitter_id=twitter_id, screen_name=profile.screen_name, friends_count=profile.friends_count, followers_count=profile.followers_count, location=profile.location)
							twitter_user_instance = self.get_twitter_user(twitter_id=twitter_id)
							profile_instance.add_follower(twitter_user_instance)
							profile_instance.save()
			except Exception, RateLimited:
				self.change_status_to_rate_limited(auth_set_instance)
				self.get_api()

	def get_api(self):
		auth_sets = OauthSet.objects.filter(active=False, rate_limited=False)
		if auth_sets:
			auth_set = auth_sets[0].id
			consumer_key = auth_sets[0].c_key
			consumer_secret = auth_sets[0].c_secret
			oauth_token = auth_sets[0].access_key
			oauth_secret = auth_sets[0].access_secret
			auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(oauth_token, oauth_secret)
			active_true = auth_sets[0].active == True
			auth_sets[0].save()
			return {"auth":tweepy.API(auth), "auth_set":auth_set}
		else:
			self.sleep_action()

	def sleep_action(self):
		sleep(random.randint(10,60))

	def sleep_on_start(self):
		sleep(random.randint(1,2))

	def sleep_15(self):
		sleep(15*60)

	def get_list_subscribers(self, job):
		job_id = job.id
		list_instance = job.twitter_list
		list_name = job.twitteR_list.name.split(',')
		list_owner = job.twitter_list.owner
		twitter_list_id = job.twitter_list.twitter_id
		api = self.get_api()
		for name in list_name:
			twitter_list_name = name
			list_instance = list_instance
			owner = list_owner
			subscribers = api.list_members(list_id = twitter_list_id)
			for subscriber in subscribers:
				try:
					screen_name = subscriber.screen_name
					twitter_id = subscriber.id
					followers_count = subscriber.followers_count
					friends_count = subscriber.friends_count
					location = subscriber.location
					twitter_user, created = TwitterUser.objects.get_or_create(screen_name = screen_name, twitter_id=twitter_id, followers_count = followers_count, freinds_count = friends_count)
					twitter_user.save()
					twitter_user = TwitterUser.objects.get(pk=twitter_id)
					new_relationship, created = TwitterRelationship.objects.get_or_create(twitterUser=twitter_user, action="SUBSCRIBE", twitter_list= list_instance)
					relationship_id = new_relationship.id
					get_relationship = TwitterRelationship.objects.get(pk=relationship_id)
					add_subscriber = twitter_user.twitterrelationship_set.add(get_relationship, "SUBSCRIBE")
					add_subscriber.save()
				except Exception, e:
					print e
			this_job = Job.objects.get(pk=job_id)
			this_job.is_complete = True
			this_job.save()

	def get_profile_instance(self, profile_id):
		twitter_profile = Profile.objects.get(pk=profile_id)
		if twitter_profile:
			return twitter_profile
		else:
			twitter_profile = Profile.objects.create(twitter_id = profile_id)
			twitter_profile.save()
			get_twitter_profile = Profile.objects.get(twitter_id = profile_id)
			return get_twitter_profile
	
	def get_twitter_user_instance(self, screen_name):
		twitter_user = TwitterUser.objects.get(screen_name=twitter_id)
		if twitter_user:
			return twitter_user
		else:
			twitter_user = TwitterUser.objects.create(screen_name=screen_name)
			twitter_user.save()
			get_twitter_user = TwitterUser.objects.get(screen_name = screen_name)
			return get_twitter_user

	def get_lists(self, job):
		job_id = job.id
		account = self.account
		list_owners = job.owner.split(',')
		profile_id = job.socialprofile.profile_id
		profile = self.get_profile_instance(profile_id)
		api = self.get_api()
		for owner in list_owners:
			try:
				user = self.get_twitter_user_instance(owner)
				all_lists = api.lists_all(owner)
				for l in all_lists:
					if l:
						user.has_list = True
						user.save()
						twitter_list = TwitterList.objects.create(name=l.name, twitter_id = l.id, profile=profile, owner=user)
						twitter_list.save()
						twitter_list = TwitterList.objects.get(twitter_id=l.id)
						Job.objects.create(socialprofile=self.account, action=)
					else:
						self.sleep_action()
			except Exception, RateLimited:
				print RateLimited
		this = Job.objects.get(pk=job_id)
		this.is_complete = True
		this.save()
		self.sleep_action()


		

	def run(self):
		get_twitter_lists = self.jobs.filter(action="GET_LISTS")
		get_list_subscribers = self.jobs.filter(action="GET_LIST_SUBSCRIBERS")
		get_user_accounts = self.jobs.filter(action="GET_ACCOUNT_INFO")
		for job in get_user_accounts:
			job.action = self.FetchAccount
			job.action(job)

		for job in get_list_subscribers:
			job.action = self.get_list_subscribers
			job.action(job)

		for job in get_twitter_lists:
			job.action = self.get_twitter_lists
			job.action(job)






