from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
	pass

	def get_latest_notifications(self):
		return self.notifications.all()[:5]

	def notifications_unseen_count(self):
		return self.notifications.filter(seen=False).count()

class SocialProfile(models.Model):
	BACKEND_CHOICES = (
		('twitter', 'Twitter'),
		('instagram', 'Instagram'),
		)
	profile = models.ForeignKey(Profile, related_name="accounts")
	provider = models.CharField(max_length=30, choices=BACKEND_CHOICES, blank=True, null=True)
	handle = models.CharField(max_length=50, blank=True, null=True)
	token = models.CharField(max_length=100, blank=True, null=True)
	secret = models.CharField(max_length=100, blank=True, null=True)
	is_executing_jobs = models.BooleanField(default=False)
	first_query = models.BooleanField(default=True)
	last_query = models.DateTimeField(auto_now=True, default=None, null = True, blank=True)
	friend_count = models.IntegerField(default = None, null = True)
	last_follower = models.IntegerField(default = None, null = True)
	follower_count = models.IntegerField(default=None, null = True)
	new_followers = models.IntegerField(default = None, null = True)
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
		self.remove_relationship(twitterUser, "FRIEND")

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