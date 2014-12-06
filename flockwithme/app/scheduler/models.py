from django.db import models
from flockwithme.core.profiles.models import Profile, SocialProfile
from django.dispatch import receiver
from django.db.models.signals import post_save

class TwitterStatus(models.Model):
	twitter_id = models.BigIntegerField()
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	text = models.CharField(max_length=160)
	hashtags = models.ManyToManyField('Hashtag', related_name='statuses', blank=True, null=True)
	favorite_count = models.PositiveIntegerField(blank=True, null=True)
	retweet_count = models.PositiveIntegerField(blank=True, null=True)
	twitter_user = models.ForeignKey('TwitterUser', blank=True, null=True)
	relationships = models.ManyToManyField(SocialProfile, through='TwitterRelationship')


	def __unicode__(self):
		return unicode(self.twitter_id)

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

	def __unicode__(self):
		return unicode(self.screen_name)


class TwitterRelationship(models.Model):
	ACTION_CHOICES = (
		('FOLLOWER', 'Follower'),
		('FRIEND', 'Friend'),
		('UNFRIEND', 'Unfriended'),
		('FAVORITE', 'Favorite'),
		('DM', 'Direct Message'),
		)
	action = models.CharField(choices=ACTION_CHOICES, max_length=20)
	socialProfile = models.ForeignKey(SocialProfile, related_name='relationships')
	twitterUser = models.ForeignKey(TwitterUser, blank=True, null=True)
	twitterStatus = models.ForeignKey(TwitterStatus, blank=True, null=True)
	message = models.CharField(max_length=160, null=True, blank=True)
	is_initial = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)


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
	favorites_count = models.PositiveIntegerField(blank = True, null = True)
	tweet_count = models.PositiveIntegerField(blank = True, null = True)
	created_at = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return unicode(self.screen_name)

class TwitterList(models.Model):
	name = models.CharField(max_length = 100, blank = True, null = True)
	profile = models.ForeignKey(Profile, related_name = "profile_lists", blank = True, null = True)
	owner = models.ForeignKey(TwitterUser, related_name = "Twitter_List_Owner", default = None)
	subscribers = models.ManyToManyField(TwitterUser, related_name = "List_Subscribers", default = None)
	created_at = models.DateTimeField(auto_now_add = True)


	def __unicode__(self):
		return self.name
	def get_owner(self):
		return unicode(self.owner)
	def get_profile(self):
		return self.profile.username

	def get_list_subscribers(self):
		return self.subscribers.screen_name


class Job(models.Model):
	ACTION_CHOICES = (
		("FOLLOW_HASHTAG", "Follow users based on hashtags"),
		("FOLLOW_BACK", "Follow back your followers"),
		("FAVORITE", "Favorite tweets"),
		("UNFOLLOW_BACK", "Unfollow all the users that haven't followed you back"),
		("UNFOLLOW_ALL", "Unfollow everyone you currently follow"),
		("AUTO_DM", "Send direct messages to your followers"),
		("FOLLOW_INFLUENCER", "Follow people who follow certain accounts."),
		("FOLLOW_MEMBERS_OF_LIST", "Follow the members of a specific list"),
		("TRACK_FOLLOWERS", "Track followers"),
		("GET_FOLLOWERS", 'get_followers'),
		("GET_LISTS", 'get_lists',)
		)
	socialprofile = models.ForeignKey(SocialProfile, related_name='jobs')
	action = models.CharField(max_length=20, choices=ACTION_CHOICES, blank=True, null=True)
	message = models.CharField(max_length=160, blank=True, null=True)
	hashtag = models.ForeignKey(Hashtag, related_name='hashtags', blank=True, null=True)
	location = models.ForeignKey(Location, related_name='locations', blank=True, null=True)
	radius = models.PositiveIntegerField(blank=True, null=True)
	number = models.PositiveIntegerField(blank=True, null=True)
	influencer = models.ForeignKey(Influencer, related_name = 'influencers', blank = True, null = True)
	twitter_list = models.ForeignKey(TwitterList, related_name = 'twitter_list_job', blank= True, null = True)

	def __unicode__(self):
		return unicode("%s for %s" % (self.action, self.socialprofile))

@receiver(post_save, sender=SocialProfile)
def run_analysis(sender, **kwargs):
	if kwargs.pop('created'):
		job = Job.objects.create(action="TRACK_FOLLOWERS", socialprofile=kwargs['instance'], number=1)
		job.save()