from django.db import models
from flockwithme.core.profiles.models import Profile, SocialProfile
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
import time

class TwitterStatus(models.Model):
	twitter_id = models.BigIntegerField()
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	text = models.CharField(max_length=160)
	hashtags = models.ManyToManyField('Hashtag', related_name='statuses', blank=True, null=True)
	favorite_count = models.PositiveIntegerField(blank=True, null=True)
	retweet_count = models.PositiveIntegerField(blank=True, null=True)
	twitter_user = models.ForeignKey('TwitterUser', blank=True, null=True)
	relationships = models.ManyToManyField(SocialProfile, through='TwitterRelationship')
	favorited_by= models.ForeignKey(SocialProfile, related_name='Favorite_Statuses', blank=True, null=True)

	class Meta:
		ordering = ['-created_at']
	def __unicode__(self):
		return unicode(self.twitter_id)

class ApiStatus(models.Model):
	STATUS_TYPES = (
		('Active', "active"),
		('Rate_Limited', 'rate_limited'),
		)
	status = models.CharField(max_length=20, choices=STATUS_TYPES, default="Active")

class OauthSet(models.Model):
	name = models.CharField(max_length=250, default="TokenSet%d")
	c_key = models.CharField(max_length=250, default=False)
	c_secret = models.CharField(max_length=250, default=False)
	access_key = models.CharField(max_length=250, default=False)
	key_secret = models.CharField(max_length=250, default=False)
	active = models.BooleanField(default=False)
	rate_limited = models.BooleanField(default=False)
	last_used = models.DateTimeField(auto_now=True, null=True)
	
	def __unicode__(self):
		return self.name%(self.id)
	
	def get_last_used(self):
		print dir(last_used)
	def get_id(self):
		return self.id
	def being_used(self):
		return self.being_used

	def consumer_key(self):
		return self.consumer_key

	def consumer_secret(self):
		return self.consumer_secret

	def access_token(self):
		return self.access_token
	def access_secret(self):
		return self.access_secret

class TwitterUser(models.Model):
	screen_name = models.CharField(max_length=40, blank=True, null=True)
	twitter_id = models.BigIntegerField(primary_key=True)
	verified = models.BooleanField(default=False)
	followers_count = models.PositiveIntegerField(blank=True, null=True)
	favorites_count = models.PositiveIntegerField(blank=True, null=True)
	friends_count = models.PositiveIntegerField(blank=True, null=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	statuses_count = models.PositiveIntegerField(blank=True, null=True)
	relationships = models.ManyToManyField(SocialProfile, through='TwitterRelationship')
	has_list = models.BooleanField(default=False)
	is_queried = models.BooleanField(default=False)
	def __unicode__(self):
		return unicode(self.screen_name)

	def get_queried(self):
		return self.is_queried

	def has_lists(self):
		return self.has_lists

class TwitterList(models.Model):
	name = models.CharField(max_length = 100, blank = True, null = True)
	owner = models.ForeignKey('TwitterListOwner', related_name = "Owner_Of_List", default = None)
	is_queried = models.BooleanField(default=False)
	#members of the list on twitter
	subscribers = models.ManyToManyField(TwitterUser, through="TwitterRelationship", related_name = "List_Subscribers", default = None)
	created_at = models.DateTimeField(auto_now_add = True)
	twitter_id = models.IntegerField(null = True, blank = True)
	#user instances that have this list as a source for following accounts
	followers = models.ManyToManyField(Profile, related_name="List_following", )

	def __unicode__(self):
		return self.name
	def get_owner(self):
		return unicode(self.owner)
	def get_profile(self):
		return self.profile.username
	def get_profile_id(self):
		return self.profile.id
	def get_list_subscribers(self):
		return ' '.join(str(x.screen_name) for x in self.subscribers.all())
	
	def get_id(self):
		return self.id
	def get_subscriber_count(self):
		return len(self.subscribers.all())

class TwitterRelationship(models.Model):
	ACTION_CHOICES = (
		('FOLLOWER', 'Follower'),
		('FRIEND', 'Friend'),
		('UNFRIEND', 'Unfriended'),
		('FAVORITE', 'Favorite'),
		('DM', 'Direct Message'),
		('SUBSCRIBE', 'Subscriber'),
		('TWEET', 'Tweet'),
		)
	action = models.CharField(choices=ACTION_CHOICES, max_length=20)
	socialProfile = models.ForeignKey(SocialProfile, null=True, blank=True, related_name='relationships')
	twitterUser = models.ForeignKey(TwitterUser, blank=True, null=True)
	influencer = models.ForeignKey('Influencer', blank=True, null=True, related_name='relationships')
	twitterStatus = models.ForeignKey(TwitterStatus, blank=True, null=True)
	twitterList = models.ForeignKey(TwitterList, blank=True, null = True)
	TwitterListOwner = models.ForeignKey('TwitterListOwner', blank = True, null = True)
	message = models.CharField(max_length=160, null=True, blank=True)
	is_initial = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
class Location(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	profiles = models.ManyToManyField(Profile, related_name='locations', blank=True ,null=True)

	def __unicode__(self):
		return unicode(self.name) if self.name else unicode((self.latitude, self.longitude),)


class Hashtag(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True, unique=True)
	profiles = models.ManyToManyField(Profile, related_name='hashtags', blank=True, null=True)

	def __unicode__(self):
		return unicode(self.name)

class Influencer(models.Model):
	profiles = models.ManyToManyField(Profile, related_name = "influencers", blank = True, null = True)
	twitter_id = models.BigIntegerField(blank = True, null = True)
	screen_name = models.CharField(max_length = 250, blank = False, null = False)
	followers_count = models.PositiveIntegerField(blank = True, null = True)
	friends_count = models.PositiveIntegerField(blank=True, null=True)
	favorites_count = models.PositiveIntegerField(blank = True, null = True)
	tweet_count = models.PositiveIntegerField(blank = True, null = True)
	created_at = models.DateTimeField(auto_now_add = True)
	been_queried = models.BooleanField(default=False)
	def __unicode__(self):
		return unicode(self.screen_name)


 
class TwitterListOwner(models.Model):
	#The Screen name is what the profile will submit
	screen_name = models.CharField(max_length=250)
	#Used by the ListFetcher to determine which ListOwners have been queiried for lists and which ones haven't
	is_queried = models.BooleanField(default=False)
	#if the user submits a twitterlist owner that doesn't actually have any lists. This will change to False. 
	owns_lists = models.BooleanField(default=True)
	#we want twitterlistowners to be accessible through profile. Users are either following TwitterListOwners (and as a result the lists they own) or not
	followers = models.ManyToManyField(Profile, related_name="owners", blank=True, null=True)
	#the twitter profile is the twitter_user_instance in our database
	#By default this will be left blank
	twitter_profile = models.ForeignKey(TwitterUser, related_name="twitter_list_owners", blank=True, null=True)


	def __unicode__(self):
		return self.screen_name

class Job(models.Model):
	ACTION_CHOICES = (
		("FOLLOW", 'Follow'),
		('FOLLOW_FAV', "Follow users and favorite tweets"),
		("FAVORITE", "Favorite tweets"),
		("UNFOLLOW", "Unfollow all the users that haven't followed you back"),
		("AUTO_DM", "Send direct messages to your followers"),
		("TRACK_FOLLOWERS", "Track followers"),
		("GET_ACCOUNT_INFO", "get_account_info"),
		)

	JOB_CHOICES = (("AUTO_PILOT", 'AUTO_PILOT'))
	socialprofile = models.ForeignKey(SocialProfile, related_name='jobs')
	job_type = models.CharField(choices=JOB_CHOICES, max_length=20)
	action = models.CharField(max_length=20, choices=ACTION_CHOICES, blank=True, null=True)
	message = models.CharField(max_length=160, blank=True, null=True)
	follow_timestamp = models.DateTimeField()
	favorite_timestamp = models.DateTimeField()
	dm_timestamp = models.DateTimeField()
	unfollow_timestamp = models.DateTimeField()
	hashtag = models.ForeignKey(Hashtag, related_name='hashtags', blank=True, null=True)
	location = models.ForeignKey(Location, related_name='locations', blank=True, null=True)
	radius = models.PositiveIntegerField(blank=True, null=True)
	number = models.PositiveIntegerField(blank=True, null=True)
	influencer = models.ForeignKey(Influencer, related_name = 'influencers', blank = True, null = True)
	owner = models.CharField(max_length=250, null = True, blank = True)
	twitter_list = models.ForeignKey(TwitterList, related_name = 'twitter_lists', blank=True, null = True)
	is_complete = models.BooleanField(default=False)
	def __unicode__(self):
		return unicode("%s for %s" % (self.action, self.socialprofile))



@receiver(post_save, sender=SocialProfile)
def run_analysis(sender, **kwargs):
	if kwargs.pop('created'):
		job = Job.objects.create(action="TRACK_FOLLOWERS", socialprofile=kwargs['instance'], number=1)
		job.save()