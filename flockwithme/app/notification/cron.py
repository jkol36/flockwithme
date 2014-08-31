from django.db.models import Q
from django.utils import timezone
from flockwithme.app.scheduler.models import 
from flockwithme.core.profiles.models import SocialProfile
from .models import Notification
import kronos


 @kronos.register('59 23 * * *')
 def send_notifications():
 	now = timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)
 	for acc in SocialProfile.objects.all():
 		num_followers = acc.relationships.filter(
 			twitterrelationship__created_at__gte=now,
 			twitterrelationship__action="FOLLOWER").count()
 		if num_followers > 0:
 			Notification.objects.create(message="You've gained %d followers today!")