import os
import sys
from optparse import OptionParser
from django.conf import settings
import time
import tweepy
from tweepy.error import TweepError
from flockwithme.app.scheduler.models import OauthSet, Influencer, TwitterUser, TwitterRelationship, TwitterStatus, Hashtag
from flockwithme.core.profiles.models import SocialProfile
from threading import Thread

#a class with all our Twitter Get Methods
class TwitterGetFunctions(object):
	def __init__(self, socialprofile=None, influencer=None, screen_name=None, *args, **kwargs):
		self.socialprofile = socialprofile
		self.influencer = influencer
		self.screen_name = screen_name
		super(TwitterGetFunctions, self).__init__()
	
	def get_api(self):
		self.access_token = self.socialprofile.token
		self.access_token_secret = self.socialprofile.secret
		self.consumer_key = '3Gsg8IIX95Wxq28pDEkA'
		self.consumer_secret = "LjEPM4kQAC0XE81bgktdHAaND3am9tTllXghn0B639o"
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		return self.api
	
	def get_tweets(self, screen_name=None, is_initial=False):
		self.api = self.get_api()
		if not self.screen_name:
			try:
				tweets = tweepy.Cursor(self.api.user_timeline).items()
			except TweepError as e:
				self.process_e = self.process_exception(e)
			for status in tweets:
				self.process_status(status)
				
		return tweepy.Cursor(self.api.user_timeline, screen_name=self.screen_name).items()
		
	def process_status(self, status):
		self.hashtags = [x for x in status.entities.hashtags]
		self.tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id = status.id, text=status.text.encode('utf-8'), favorite_count = status.favorite_count, retweet_count=status.retweet_count)
		self.tstatus.save()
		if not self.hashtags:
			return self.tstatus
		for hashtag in self.hashtags:
			self.h, _ = Hashtag.objects.get_or_create(name=hashtag, twitterStatus=self.tstatus) 
			self.h.save()
		return self.tstatus


	def get_followers(self, screen_name=None, is_initial=False):
		if not self.screen_name:
			self.twitter_followers = tweepy.Cursor(self.api.followers_ids).items()
			for twitter_id in self.twitter_followers:
				tuser, _ = TwitterUser.objects.get_or_creat(twitter_id=twitter_id)
				tuser.save()
				self.socialprofile.add_follower(tuser)
				self.socialprofile.save()
			return "Done"

		self.twitter_followers = tweepy.Cursor(self.api.followers_ids, screen_name=screen_name).items()
		for twitter_id in self.twitter_followers:
			self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
			self.tuser.save()
			self.relationship, _ = TwitterRelationship.objects.get_or_create(influencer=self.influencer, twitterUser=self.Tuser, action="FOLLOWER")
			self.relationship.save()
			self.influencer.save()
		return "Done"

	def get_friends(self, screen_name=None, is_initial=False):
		if not self.screen_name:
			self.twitter_friends = tweepy.Cursor(self.get_api.followers_ids).items()
			for twitter_id  in self.twitter_friends:
				tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
				tuser.save()
				self.socialprofile.add_friend(tuser, is_initial=self.is_initial)
				self.socialprofile.save()
			return "Done"
		self.twitter_friends = tweepy.Cursor(self.get_api.followers_ids, screen_name=self.screen_name)
		for twitter_id in self.twitter_friends:
			self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=twitter_id)
			self.tuser.save()
			self.new_relationship = TwitterRelationship.objects.get_or_create(influencer=self.influencer, twitterUser=self.tuser, action="FRIEND", is_initial=self.is_initial)
			self.new_relationship.save()
			self.influencer.save()
		return "Done"

	def get_favorites(self, screen_name=None, is_initial=False):
		if not self.screen_name:
			self.favorites = tweepy.Cursor(self.get_api.favorites).items()
			for status in self.favorites:
				self.Tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id=status.id, text=status.text.encode('utf-8'), favorite_count=status.favorites_count, retweet_count=status.retweet_count)
				self.Tstatus.save()
				self.socialprofile.add_favorite(self.Tstatus, is_initial=self.is_initial) 
				self.socialprofile.save()
			return "Done"
		self.favorites = tweepy.Cursor(self.get_api().favorites, screen_name=self.screen_name)
		for status in self.favorites:
			self.Tstatus, _ = TwitterStatus.objects.get_or_create(twitter_id=status.id, text=status.text.encode('utf-8'), favorite_count=status.favorites_count, retweet_count=status.retweet_count)
			self.Tstatus.save()
			self.new_relationship, _ = TwitterRelationship.objects.get_or_create(twitterStatus=self.Tstatus, influencer=self.influencer, action="FAVORITE", is_initial=self.is_initial)
			self.new_relationship.save()
			self.influencer.save()
		return "Done"
	#followers, Friends, Tweets
	def get_everything(self, screen_name=None, is_initial=False):
		self.api = self.get_api()
		self.is_initial = is_initial
		print self.socialprofile
		#if is_initial == False we'll query twitter for followers, friends, and tweets and add them to the database
		

		print "is_initial = {}".format(self.is_initial)
		#if is initial is false we can assume that the user does not have any database followers, or tweets, or friends.

		#get_my_followers
		####print "getting followers"
		####try:
		####	self.twitter_followers = tweepy.Cursor(api.followers_ids).items()
		####except TweepError, e:
		####	process_e = self.process_exception(e)
		
		####try:
			####for follower in self.twitter_followers:
			####	self.followers_to_be_added.append(follower)
		####except TweepError, e:
			#self.process_e = self.process_exception(e)
		

		#####get_my_following:
		####print "getting following"
		####try:
		####	self.following = tweepy.Cursor(api.friends_ids).items())
		####except TweepError, e:
		####	self.process_e = self.process_exception(e)
		
		
		####if not len(self.following) > 0:
		####	print "No friends"

		####for friend in self.following:
		####	try:
		####		self.friends_to_be_added.append(friend)
		####	except Exception, e:
		####		process_e = self.process_exception(e)
		####

		########CLEANING TIME ###########
		#2. clean friends
		###if not len(self.friends_to_be_added) > 1:
		###	return "No_New_Friends"
		###elif not len(self.followers_to_be_added) > 1:
		###	return "No_New_Followers"
		###else:
			#compare the users friends on Twitter to his Friends in the database
			#add the ones that are present in his list of following on Twitter but aren't present in his list of following in our flock db.
			##self.db_friends = [x.twitterUser.twitter_id for x in self.socialprofile.get_friends()]
			##self.friends_to_add = [x for x in self.friends_to_be_added if x not in self.db_friends]
			##self.followers_to_add = [x for x in self.followers_to_be_added if x not in self.db_followers]
			#if there are no friends to add return no friends to write to db
			##if not len(self.friends_to_add) > 1:
				##return "No Friends to Write to DB"
			#If there are no followers to write to the database
			##elif not len(self.followers_to_be_added) > 1:
				##return 'No followers to write to the database'

			#otherwise, for id in friends.
			##for friend in self.friends_to_add:
				##try:
					##tuser, _ = TwitterUser.objects.get_or_create(twitter_id=friend) 
				##except Exception, e:
					##self.process_e = self.process_exception(e)
				#tuser.save()
				#self.socialprofile.add_friend(tuser, is_initial=self.is_initial)
				#self.socialprofile.save()
				#if len(self.followers_to_be_added) > 1:
					#self.db_followers = [x.twitterUser.twitter_id for x in self.socialprofile.get_followers()]
					#self.should_add = [x for x in self.followers_to_be_added if x not in self.db_followers]
					#if len(self.should_add) > 1:
						#for user in self.should_add:
							#try:
								#self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=user)
							#except Exception, e:
							#	self.process_e = self.process_exception(e)
							#self.tuser.save()
							#self.socialprofile.add_follower(self.tuser, is_initial=True)
							#self.socialprofile.save()
					#else:
						#self.socialprofile.job_status = "Account_Info_Fetched"
						#self.socialprofile.save()
				#else:
					#self.socialprofile.job_status = 'Account_Info_Fetched'
					#self.socialprofile.save()
			

			##otherwise do this
			#else:
				#if len(self.followers_to_be_added) > 1:
					#self.db_followers = [x.twitterUser.twitter_id for x in self.socialprofile.get_followers()]
					#self.should_add = [x for x in self.followers_to_be_added if x not in self.db_followers]
					#if self.should_add > 1:
						#for user in self.should_add:
							#try:
								#self.tuser, _ = TwitterUser.objects.get_or_create(twitter_id=user)
							#except Exception, e:
								#self.process_e = self.process_exception(e)

							#self.tuser.save()
							#self.socialprofile.add_follower(self.tuser, is_initial=True)
						#self.socialprofile.save()

		



	def process_exception(self, e):
		if "Rate limit exceeded" in str(e):
			print 'rate limited, sleeping'
			time.sleep(900)
		else:
			print 'error'
		
	


class FetchSocialProfileInfo(Thread, TwitterGetFunctions):
	def __init__(self, is_initial=False, *args, **kwargs):
		self.queue = kwargs.pop('queue')
		self.socialprofile = kwargs.pop('socialprofile')
		self.action = kwargs.pop('action')
		self.is_initial = is_initial
		print self.is_initial
		self.queue.put(self)
		TwitterGetFunctions.__init__(self, socialprofile=self.socialprofile,  *args, **kwargs)
		super(FetchSocialProfileInfo, self).__init__(*args, **kwargs)

	def run(self):
		if self.action == "Get_Everything":
			self.action = self.get_everything(is_initial=self.is_initial)
		elif self.action == "Get_Tweets":
			self.action = self.get_tweets(is_initial=self.is_initial)
		elif self.action == "Get_Followers":
			self.action = self.get_followers()

class FetchInfluencerInfo(Thread, TwitterGetFunctions):
	def __init__(self, *args, **kwargs):
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
			self.action = self.get_everything(influencer=self.influencer, screen_name=self.screen_name)

		elif self.action == "Get_Followers":
			self.action = self.get_followers(influencer=self.influencer, screen_name=self.screen_name)

		elif self.action == "Get_Tweets":
			self.action = self.get_tweets(influencer=self.influencer, screen_name=self.screen_name)

		elif self.action == "Get_Favorites":
			self.actioon = self.get_favorites(influencer=self.influencer, screen_name=self.screen_name)

		elif self.action == "Get_Friends":
			self.action = self.get_friends(influencer=self.influencer, screen_name=self.screen_name)

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

