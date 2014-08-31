from django.db import models
from flockwithme.core.profiles.models import Profile

class Notification(models.Model):
	receiver = models.ForeignKey(Profile, related_name='notifications')
	message = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)

	def short_message(self):
		return self.message[:30]

	def __unicode__(self):
		return unicode(self.receiver)