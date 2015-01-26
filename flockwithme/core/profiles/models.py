from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
	pass

	def get_latest_notifications(self):
		return self.notifications.all()[:5]

	def notifications_unseen_count(self):
		return self.notifications.filter(seen=False).count()

	PROFILE_STATUS = (
		('active', 'Congratulations! All your Twitter Accounts are currently running on auto-pilot! Go out and play or something.'),
		('pending', 'all actions are currently pending. If this message lasts for more than 24 hours. Please contact us.'),
		('paused', 'actions are currently paused for all your accounts.'),
		)
	profile_status = models.CharField(max_length=250, default="pending", choices=PROFILE_STATUS)

class SocialProfile(models.Model):
	BACKEND_CHOICES = (
		('twitter', 'Twitter'),
		('instagram', 'Instagram'),
		)
	JOB_STATUS = (
		('Just_Cleaned', 'We just fixed up your following/follower ratio. Next up, is to follow people and favorite tweets.'),
		('Dm_Skipped', "We couldn't direct message your followers because you didn't set a message. This process was skipped today."),
		#sleep until tomorrow
		('Just_Dmed', "We just sent your message to your most recent followers. All actions complete for today."),
		#favorite tweets and auto dm
		('Follow_Limit_Reached', "Following people failed because you're rate limited. We'll try again tomorrow."),
		#clean follow ratio
		('Follow_Ratio_Off', "Following people failed because you're following to many people. Next up is to clean up your ratio!"),
		('Fetch_Account_Info', "Next Up is to fetch your followers and friends."),
		('Fetching_Account_Info', 'Currently fetching your friends and followers.'),
		#clean Account
		('Account_Info_Fetched', 'We finished Fetching your account info. Next up is to check your follow ratio and clean up your account if neccessary.' ),
		#Follow users
		('Ratio_Good', "Just checked your Following/Follower ratio and everything is good! Next up is to follow people and favorite Tweets."),
		#clean account
		('Ratio_Bad', 'Your Ratio needs cleaning.'),
		#Favorite Tweets
		('FAVORITES_FETCHED', 'ready to favorite tweets'),
		#Send Direct Messages to followers
		("Just_Favorited", 'We just favorited tweets. Next Step is to auto_dm your followers.'),
		#prompt the user for action
		("Ratio_Dirty_No_Unfollowers", "Your ratio is dirty and you have no one who is not following you."),
		#try favoriting tweets.
		("No_Users_To_Follow", "That's weird. Following users failed because we couldn't find people to follow."),
		)
	profile = models.ForeignKey(Profile, related_name="accounts")
	job_status = models.CharField(max_length=150, choices=JOB_STATUS, default='Fetch_Account_Info')
	provider = models.CharField(max_length=30, choices=BACKEND_CHOICES, blank=True, null=True)
	handle = models.CharField(max_length=50, blank=True, null=True)
	twitter_id = models.IntegerField(default=None, null=True)
	token = models.CharField(max_length=100, blank=True, null=True)
	secret = models.CharField(max_length=100, blank=True, null=True)
	is_executing_jobs = models.BooleanField(default=False)
	followers_count = models.IntegerField(default=None, null=True)
	friend_count = models.IntegerField(default = None, null = True)
	def get_followers(self, is_initial=True):
		return self.relationships.filter(action="FOLLOWER", socialProfile=self, is_initial=is_initial).all()

	def get_friends(self):
		return self.relationships.filter(action="FRIEND", socialProfile=self).all()

	def get_unfriended(self):
		return self.relationships.filter(action="UNFRIEND", socialProfile=self).all()

	def get_favorites(self):
		return self.relationships.filter(action="FAVORITE", socialProfile=self).all()

	def get_dms(self):
		return self.relationships.filter(action="AUTO_DM", socialProfile=self).all()

	def add_dm(self, twitterUser, message):
		self.add_relationship(twitterUser, "AUTO_DM", message=message)

	def add_friend(self, twitterUser):
		self.add_relationship(twitterUser, "FRIEND")

	def add_follower(self, twitterUser, is_initial=False):
		self.add_relationship(twitterUser, "FOLLOWER", is_initial=is_initial)

	def add_unfriend(self, twitterUser):
		self.add_relationship(twitterUser, "UNFRIEND")

	def delete_friend(self, twitterUser):
		self.relationships.remove(twitterUser, "FRIEND")

	def add_favorite(self, twitterStatus):
		self.add_relationship(twitterStatus, "FAVORITE", status=True)

	def add_relationship(self, receiver, action, message=None, status=False, is_initial=False):
		model = models.get_model('scheduler', 'TwitterRelationship')
		if action == "AUTO_DM":
			model.objects.get_or_create(socialProfile=self, twitterUser=receiver, action=action, message=message)	
		elif status:
			model.objects.get_or_create(socialProfile=self, twitterStatus=receiver, action=action)
		else:
			model.objects.get_or_create(socialProfile=self, twitterUser=receiver, action=action, is_initial=is_initial)

	def __unicode__(self):
		return unicode('%s - %s' % (self.handle, self.get_provider_display()))