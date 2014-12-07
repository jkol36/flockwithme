# -*- coding: utf-8 -*-
import tweepy	
from threading import Thread
from django.conf import settings
from .models import *
from flockwithme.core.profiles.models import SocialProfile
from time import sleep
from flockwithme.app.scheduler.models import TwitterList
import random
import logging
logger = logging.getLogger(__name__)


class JobExecuter(Thread):
	def __init__(self, lock=None, *args, **kwargs):
		self.queue = kwargs.pop('queue')
		self.account = kwargs.pop('account')
		self.jobs = kwargs.pop('jobs')
		self.lock = lock
		try:
			if self.jobs.filter(action="TRACK_FOLLOWERS").count() == 0:
				self.sleep_on_start()
			else:
				pass
		except tweepy.TweepError as e:
			logger.error("\nUSER: %s, ERROR: %s" % (self.account.handle, e))
			self.queue.put(self)
		return super(JobExecuter, self).__init__(*args, **kwargs)
		self.daemon = True
		self.api = self.get_api()

	def sleep_action(self):
		sleep(random.randint(10,60))

	def sleep_on_start(self):
		sleep(random.randint(1,2))

	def auto_follow(self, job):
		statuses = job.hashtag.statuses.all().exclude(twitter_user__twitter_id__in=[x.twitterUser.twitter_id for x in self.account.get_friends()])[0:(job.number*10)]
		users = list(set([status.twitter_user for status in statuses][0:job.number]))
		for user in users:
			try:
				self.api.create_friendship(user.twitter_id, follow=False)
				self.account.add_friend(user)
				self.sleep_action()
			except tweepy.TweepError as e:
				if self.handle_error(e):
					break

		self.account.save()

	def unfollow_back(self, job):
		friends = set(self.api.friends_ids())
		followers = set(self.api.followers_ids())		
		should_unfollow = friends-followers
		unfollowed = 0
		for profile in should_unfollow:
			if unfollowed < 3000:
				try:
					self.api.destroy_friendship(profile)
					print 'successfully unfollowed %d' %(profile)
					unfollowed += 1
					twitterUser, _ = TwitterUser.objects.get_or_create(twitter_id=profile)
					self.account.add_unfriend(twitterUser)
				except Exception, e:
					print e
		self.account.save()
		

	def unfollow_all(self, job):
		unfollowed = 0
		friends = set(self.api.friends_ids())
		for profile in friends:
			try:
				if unfollowed < 3:
					twitterUser, _ = TwitterUser.objects.get_or_create(twitter_id=profile)
					self.api.destroy_friendship(profile)
					print "successfully unfollowed %d " %(profile)
					unfollowed += 1

					self.account.add_unfriend(twitterUser)
			except Exception, e:
				slogger.error(e)
				break
				self.sleep_status()
		
		self.account.save()
	def get_twitter_id(self, job, screen_name):
		twitter_id = self.api.get_user(screen_name=screen_name)
		print twitter_id
		return twitter_id

	def auto_favorite(self, job):
		for status in job.hashtag.statuses.all().exclude(twitter_id__in=[x.twitterStatus.twitter_id for x in self.account.get_favorites()])[0:job.number]:
			try:
				self.api.create_favorite(status.twitter_id)
				self.account.add_favorite(status)
				self.sleep_action()
			except tweepy.TweepError as e:
				try:
					code = int(e.args[0][0]['code'])
				except:
					break
				if code == 139:
					self.account.add_favorite(status)
				if self.handle_error(e):
					break

		self.account.save()
	def get_profile_instance(self, profile_id):
		twitter_profile = Profile.objects.get(pk=profile_id)
		if twitter_profile:
			return twitter_profile
		else:
			return None
	def get_twitter_user_instance(self, screen_name):
		user = TwitterUser.objects.get(screen_name=screen_name)
		if user:
			user.is_queried = True
			user.save()
			return user
		else:
			return None
	def get_lists(self, job):
		job_id = job.id
		account = self.account
		print job_id
		list_owners = job.owner.split(',')
		profile_id = job.socialprofile.profile_id
		profile = self.get_profile_instance(profile_id)
		api = self.get_api()
		for owner in list_owners:
			print owner
			user = self.get_twitter_user_instance(owner)
			all_lists = api.lists_all(owner)
			for l in all_lists:
				if l:
					user.has_list = True
					user.save()
					twitter_list = TwitterList.objects.create(name=l.name, twitter_id = l.id, profile=profile, owner=user)
					twitter_list.save()
					twitter_list = TwitterList.objects.get(twitter_id=l.id)
					Job.objects.create(socialprofile=self.account, action="GET_LIST_SUBSCRIBERS", twitter_list=twitter_list)
				else:
					self.sleep_action()
		this = Job.objects.get(pk=job_id)
		this.delete()


		'''
		profile = job.twitter_list.get_profile_id()
		get_profile = Profile.objects.get(pk=profile)
		socialprofile = SocialProfile.objects.get(profile=get_profile)
		account = get_profile
		twitter_list_id = job.twitter_list.get_id()
		api = self.get_api()
		for owner in list_owners:
			if owner:
				screen_name = owner
				twitter_lists = api.lists_all(owner)
				flock_profile = get_profile
			if twitter_lists:
				try:
					for i in twitter_lists:
						if i.name not in TwitterList.objects.all():
							print "getting twitter user object"
							get_twitter_user_object = TwitterUser.objects.get(screen_name = screen_name)
							print "got twitter user object successfully"
							print "creating twitter list object"
							object_ = TwitterList.objects.create(name=i.name, twitter_id=i.id, profile=flock_profile, owner=get_twitter_user_object)
							print "created twitter list object successfully"
							print "saving the object"
							object_.save()
							print "twitter list object saved successfully"
							print "deleting old object"
							delete_old_object = TwitterList.objects.get(pk=twitter_list_id).delete()
							print "old object deleted"
							print "creating new get list subscriber object"
							create_new_get_list_subsriber_job = Job.objects.create(action="GET_LIST_SUBSCRIBERS", twitter_list=object_, socialprofile=socialprofile )
							print "created new get list subscriber job"
							print "saving the object"
							create_new_get_list_subsriber_job.save()
							print "object saved"
							self.sleep_action()
							print "now sleeping"
						elif flock_profile not in TwitterList.objects.get(name=i.name):
							print "flock profile not in twitter list"
							print "fetching twitter list"
							twitter_list = TwitterList.objects.get(name=i.name)
							print "twitter list fetched"
							print "updating model"
							update_model = twitter_list.add(followers=flock_profile)
							print "model updated"
							print "saving model"
							update_model.save()
							print "model saved"
							self.sleep_action()

				except Exception, e:
					print e
		else:
			self.sleep_action
	'''
	def get_list_subscribers(self, job,):
		job_id = job.id
		list_instance = job.twitter_list
		list_name = job.twitter_list.name.split(',')
		list_owner = job.twitter_list.owner
		twitter_list_id = job.twitter_list.twitter_id
		api = self.get_api()
		for name in list_name:
			print name
			twitter_list_name = name
			owner = list_owner
			print owner
			print twitter_list_name
			print twitter_list_id
			subscribers = api.list_members(list_id=twitter_list_id)
			for subscriber in subscribers:
				print subscriber.screen_name
			



				
		

		
			
		





			

		

	def follow_influencer(self, job):
		screen_names = []
		screen_names_in_jobs = job.influencer.screen_name
		screen_names.append(screen_names_in_jobs)
		for screen_name in screen_names:
			twitter_id= self.api.get_user(screen_name = screen_name).id
			followers = self.api.followers_ids(id = twitter_id)
			num_followed = 0
			try:
				for follower in followers:
					twitterUser, _ = TwitterUser.objects.get_or_create(twitter_id=follower)
					self.api.create_friendship(follower)
					self.account.add_friend(twitterUser)
					num_followed +=1 
					self.sleep_action()
			except Exception, e:
				print e 
		self.account.save()

	def get_api(self):
		auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
		auth.set_access_token(self.account.token, self.account.secret)
		return tweepy.API(auth)

	def track_followers(self, job, should_dm=False):
		if job.number != 1:
			try:
				dm_job = self.account.jobs.get(action="AUTO_DM")
				should_dm = True
			except:
				should_dm = False
		current_follower_ids = [f.twitterUser.twitter_id for f in self.account.get_followers()]
		ids =  tweepy.Cursor(self.api.followers_ids).items()
		new_followers = []
		while True:
			try:
				twitter_id = next(ids)
				if twitter_id in current_follower_ids:
					return
				with self.lock:
					twitterUser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
					self.account.add_follower(twitterUser, is_initial = job.number == 1)
				new_followers.append(twitterUser)
			except StopIteration:
				break
			except tweepy.TweepError as e:
				if e.args[0][0]['code'] == 88:
					sleep(60*15)
				elif self.handle_error(e):
					return
		if should_dm:
			for user in new_followers:
				try:
					self.api.send_direct_message(user_id=user.twitter_id, message=dm_job.message)
					self.account.add_dm(user, dm_job.message)
				except tweepy.TweepError as e:
					if self.handle_error(e):
						return
		if job.number == 1:
			job.number = 0
			job.save()

	def run(self):
		## SETTING THE NUMBER OF HASHTAGS ##
		DAILY_FAV_LIMIT = 500.0
		favs = self.jobs.filter(action="FAVORITE")
		for fav in favs:
			fav.number = int(DAILY_FAV_LIMIT/favs.count())
			fav.save()
		DAILY_FOL_LIMIT = 100.0
		fols = self.jobs.filter(action="FOLLOW_HASHTAG")
		for fol in fols:
			fol.number = int(DAILY_FOL_LIMIT/fols.count())
			fol.save()
		## END NUMBERSETTING

		for job in self.jobs:
			if job.action == 'FOLLOW_HASHTAG':
				action = self.auto_follow
				job.action(job)
			elif job.action == 'FAVORITE':
				action = self.auto_favorite
				action(job)
			elif job.action == 'FOLLOW_INFLUENCER':
				action = self.follow_influencer
				job.action(job)
			elif job.action == 'TRACK_FOLLOWERS':
				action = self.track_followers
				job.action(job)
			elif job.action == 'UNFOLLOW_BACK':
				action = self.unfollow_back
				job.action(job)
			elif job.action =="UNFOLLOW_ALL":
				action = self.unfollow_all
				job.action(job)
			elif job.action == "GET_TWITTER_ID":
				job.action = self.get_twitter_id
				job.action(job)
			elif job.action =="GET_LISTS":
				job.action = self.get_lists
				job.action(job)
			elif job.action == "GET_LIST_SUBSCRIBERS":
				job.action = self.get_list_subscribers
				job.action(job)
			
			#logger.error("\nUSER: %s, ERROR: %s" % (self.account.handle, e))
		self.queue.put(self)

	def handle_error(self, e):
		try:
			code = int(e.args[0][0]['code'])
		except:
			logger.error("\nUSER: %s, ERROR: %s" % (self.account.handle, e))
			return True
		if code == 64:
			logger.error('\nUSER: %s, ERROR: User is suspended' % self.account.handle)
			return True
		if code == 32:
			logger.error('\nUSER: %s, ERROR: Page does not exist' % self.account.handle)
			return False
		if code == 88:
			logger.error('\nUSER: %s, ERROR: Rate limit exceeded' % self.account.handle)
			return True
		if code == 89:
			logger.error('\nUSER: %s, ERROR: Expired token' % self.account.handle)
			return True
		if code == 130:
			logger.error('\nUSER: %s, ERROR: Over capacity' % self.account.handle)
			return True
		if code == 131:
			logger.error('\nUSER: %s, ERROR: Twitters internal error' % self.account.handle)
			return True
		if code == 161:
			logger.error('\nUSER: %s, ERROR: You are unable to follow more people at the time' % self.account.handle)
			return True
		if code == 179:
			logger.error('\nUSER: %s, ERROR: You can not see this tweet, private user probably' % self.account.handle)
			return False
		if code == 185:
			logger.error('\nUSER: %s, ERROR: Cant tweet more, daily status limit reached' % self.account.handle)
			return True
		if code == 187:
			logger.error('\nUSER: %s, ERROR: Status is a duplicate' % self.account.handle)
			return False
		if code == 215:
			logger.error('\nUSER: %s, ERROR: Can not authenticate' % self.account.handle)
			return False