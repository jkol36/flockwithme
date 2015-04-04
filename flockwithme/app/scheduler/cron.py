import kronos
from flockwithme.core.profiles.models import Profile, SocialProfile
from flockwithme.app.scheduler.models import Influencer, Job
from Queue import Queue
from threading import Lock
from django.db.models import Q
from auto_pilot import *



@kronos.register('0 10 * * *')
def do_work():
	queue = Queue()
	for acc in SocialProfile.objects.filter(jobs__isnull=False).distinct():
		jobs = acc.jobs.all()
		print jobs
	


