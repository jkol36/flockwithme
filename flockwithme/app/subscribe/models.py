from django.db import models

class Subscriber(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	email = models.EmailField(unique=True)

	def __unicode__(self):
		return unicode(self.email)