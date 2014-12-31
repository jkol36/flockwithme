# -*- coding: utf-8 -*-
from threading import Thread
from django.conf import settings
from flockwithme.app.scheduler.models import OauthSet, TwitterUser
from flockwithme.core.profiles.models import Profile
import tweepy
from tweepy.error import TweepError
from time import sleep
import datetime
import time
import random
import logging
from .countdown import CountDown
logger = logging.getLogger(__name__)

class AccountFetch(Thread):
	def __init__(self, lock=None, *args, **kwargs):
		self.jobs = kwargs.pop('jobs')
		self.lock = lock
		self.account = kwargs.pop("account")
		self.queue = kwargs.pop("queue")
		self.api = self.get_api()
		return super(AccountFetch, self).__init__(*args, **kwargs)
		self.daemon = True
		self.queue.put(self)
	#
	def create_twitter_user(self, twitter_id, screen_name, friends_count, followers_count, location):
		new_twitter_user, created = TwitterUser.objects.get_or_create(twitter_id=twitter_id, screen_name = screen_name, friends_count=friends_count, followers_count=followers_count)
		print created
		return new_twitter_user

	def get_twitter_user(self, twitter_id):
		twitter_user_instance = TwitterUser.objects.get(twitter_id=twitter_id)
		return twitter_user_instance
	
	#On rate limited the token_set will be suspended for 15 minutes	
	def change_status_to_rate_limited(self, auth_set_id):
		rate_limited = OauthSet.objects.get(id=auth_set_id)
		rate_limited.rate_limited = True
		rate_limited.save()
 
	def change_status_from_rate_limited(self, auth_set_id):
		get_oauth_set = OauthSet.objects.get(id=auth_set_id)
		get_oauth_set.rate_limited = False
		get_oauth_set.save()

	def get_rated_limited_tokens(self):
		rate_limited_tokens = OauthSet.objects.filter(rate_limited = True)
		for token_set in rate_limited_tokens:
			time_rate_limited = token_set.last_used.replace(tzinfo=None)
			time_now = datetime.datetime.utcnow()
			difference = time_now - time_rate_limited
			total_seconds = difference.total_seconds()
			_15_min = 900.000
			#if 15 minutes have passed
			if total_seconds > _15_min:
				#Call the change_status_from_rate_limited function and pass in the token_set_id
				self.change_status_from_rate_limited(token_set.id)
			else:
				print "time now - time rate_limited = %d" %(total_seconds)
			

				

	def get_followers(self, auth):
		api = self.get_api(auth)
		follower_ids = tweepy.Cursor(api.followers_ids().items())
		return follower_ids
	
	def get_request_left(self, api):
		limit_status = api.rate_limit_status()
		requests_left = int(limit_status['resources']['followers']['/followers/ids']['remaining'])
		access_token = limit_status["rate_limit_context"]['access_token']
		return requests_left
	def FetchAccount(self, job):
		api = self.get_api()
		limit_status = api.rate_limit_status()
		requests_left = self.get_request_left(api)
		profile_instance = job.socialprofile
		twitter_username = profile_instance.profile
		first_query = job.socialprofile.first_query
		current_twitter_ids = [x.twitter_id for x in TwitterUser.objects.all()]
		if first_query == True:
			total_followers = api.get_user(screen_name=twitter_username).followers_count
			profile_instance.num_followers = total_followers
			profile_instance.first_query = False
			profile_instance.save()
		else:
			total_followers = profile_instance.num_followers
		ids = tweepy.Cursor(api.followers_ids, screen_name=profile_instance).items()
		
		should_query = []
		new_followers = profile_instance.new_followers
		#if requests
		while new_followers < total_followers:
			try:
				while requests_left:
					try:
						twitter_id = next(ids)
					except TweepError as e:
						if e.args[0][0]['code'] == 88:
							access_token = limit_status['rate_limit_context']['access_token']
							token_set = OauthSet.objects.get(access_key = str(access_token))
							#mark token set as rate limited
							token_set.rate_limited = True
							token_set.save()
							#get a new auth set for the request
							api = self.get_api()
						else:
							print e
					except Exception, e:
						print e
					else:
						if twitter_id not in current_twitter_ids:
							try:
								should_query.append(int(twitter_id))
								for twitter_id in should_query:
									print twitter_id
									profile = api.get_user(user_id=twitter_id)
									new_twitter_user = self.create_twitter_user(twitter_id=twitter_id, screen_name=profile.screen_name, friends_count=profile.friends_count, followers_count=profile.followers_count, location=profile.location)
									twitter_user_instance = self.get_twitter_user(twitter_id=twitter_id)
									self.account.add_follower(twitter_user_instance)
									self.account.save()

							except TweepError as e:
								if e.args[0][0]["code"] == 88:
									access_token = limit_status['rate_limit_context']['access_token']
									token_set = OauthSet.objects.get(access_key = str(access_token))
									#mark token set as rate limited
									token_set.rate_limited = True
									token_set.save()
									#get a new auth set for the request
									api = self.get_api()
								elif e.args[0][0]["code"] == 63:
									ids = next(ids)
								else:
									print "error line 118"
									print e
							except Exception, e:
								print "Exception"
						elif twitter_id in current_twitter_ids:
							print "twitter id in database"
							#profile = self.get_twitter_user(twitter_id=twitter_id)
							#self.account.add_follower(profile)
						else:
							print "else"
			
					
				
				access_token = limit_status['rate_limit_context']['access_token']
				token_set = OauthSet.objects.get(access_key = str(access_token))
				#mark access token as limited
				token_set.rate_limited == True
				token_set.save()
				api = self.get_api()

			except Exception, e:
				print e
			else:
				profile_instance.new_followers +=1
				profile_instance.save()

		
				

				
		
	def get_api(self):
		#first check if cooldown is up on the rate_limited tokens if cooldown is up the rate_limit will be changed to false
		cooldown = self.get_rated_limited_tokens()
		#now fetch the available oauth tokens
		auth_set = OauthSet.objects.filter(active=False, rate_limited=False)[0]
		#if there's an available token_set the system uses it for auth, otherwise sleep
		
		print "auth set found"
		print auth_set
		consumer_key = str(auth_set.c_key)
		consumer_secret = str(auth_set.c_secret)
		access_token = str(auth_set.access_key)
		access_token_secret = str(auth_set.key_secret)
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		return tweepy.API(auth)

	def sleep_action(self):
		sleep(random.randint(10,60))

	def sleep_on_start(self):
		sleep(random.randint(1,2))

	def sleep_15(self):
		sleep(15*60)

	def sleep(self):
		sleep(1)
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
						Job.objects.create(socialprofile=self.account, action="GET_LIST_SUBSCRIBERS")
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
			try:
				job.action = self.FetchAccount
				job.action(job)
			except TweepError as e:
				if e.args[0][0]["code"] == 88:
					print "sleeping line 318"
					self.sleep_action()
					continue
				elif e.args[0][0]['code'] == 63:
					self.run()
			except StopIteration:
				self.run()

		for job in get_list_subscribers:
			if job.is_complete == False:
				job.action = self.get_list_subscribers
				job.action(job)

		for job in get_twitter_lists:
			if job.is_complete == False:
				job.action = self.get_lists
				job.action(job)






