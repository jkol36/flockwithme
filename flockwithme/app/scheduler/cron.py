import kronos
from flockwithme.core.profiles.models import Profile, SocialProfile
from flockwithme.app.scheduler.models import Influencer
from .jobexecuter import JobExecuter
from .accountfetch import AccountFetch
from .Fetcher import Fetch_Twitter_Account
from Queue import Queue
from threading import Lock
from django.db.models import Q
from .auto_pilot import AutoPilot



@kronos.register('0 3 * * *')
def do_work():
	queue = Queue()
	threads = []
	passive_jobs = []
	for acct in SocialProfile.objects.filter(job_status='Account_Info_Fetched').distinct():
		threads.append(AutoPilot(account=acct, action="clean_account", queue=queue))

	for acct in SocialProfile.objects.filter(Q(job_status='Ratio_Good') | Q(job_status='Just_Cleaned')):
		threads.append(AutoPilot(account=acct, action="Follow", queue=queue))

	for acct in SocialProfile.objects.filter(job_status="Just_Followed"):
		threads.append(AutoPilot(account=acct, action="FAVORITE", queue=queue))

	for acct in SocialProfile.objects.filter(job_status="FAVORITES_FETCHED"):
		threads.append(AutoPilot(account=acct, action="FAVORITE", queue=queue))

	for acct in SocialProfile.objects.filter(job_status="Ratio_Bad"):
		threads.append(AutoPilot(account=acct, action="clean_account", queue=queue))




	for thread in threads:
		print thread
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
			print "executer works"
		except:
			executer = None
			print "executer none"
		if executer:
			threads.remove(executer)
		else:
			threads[:] = [t for t in threads if t.isAlive()]


@kronos.register('*/15 * * * *')
def track_followers():
	lock = Lock()
	queue = Queue()
	threads = []
	for acc in SocialProfile.objects.filter(jobs__isnull=False).distinct():
		if acc.is_executing_jobs:
			continue
		jobs = acc.jobs.filter(action="TRACK_FOLLOWERS")
		if jobs:
			threads.append(JobExecuter(lock=lock,account=acc, queue=queue, jobs=jobs))
	for thread in threads:
		thread.account.is_executing_jobs = True
		thread.account.save()
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer:
			threads.remove(executer)
			executer.account.is_executing_jobs = False
			executer.account.save()
		else:
			threads[:] = [t for t in threads if t.isAlive()]



@kronos.register('0 5 * * *')
def Fetch_Influencer_Followers():
	queue = Queue()
	threads = []

	for influencer in Influencer.objects.all():
		if influencer.twitter_id == None:
			threads.append(Fetch_Twitter_Account(screen_name=influencer, queue=queue, action='get_everything', model='Influencer'))
		#threads.append(Fetch_Followers(twitter_account=influencer))

	for thread in threads:
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer:
			threads.remove(executer)
		else:
			threads[:] = [t for t in threads if t.isAlive()]

@kronos.register('0 2 * * *')
def fetch_account_info():
	queue = Queue()
	threads = []

	for acc in SocialProfile.objects.filter(job_status='Fetch_Account_Info').distinct():
		threads.append(Fetch_Twitter_Account(twitter_id=acc.twitter_id, lock = Lock, queue=queue, action="get_everything", model="SocialProfile"))
		acc.job_status = 'Fetching_Account_Info'
		acc.save()

	for acc in SocialProfile.objects.filter().exclude(job_status='Fetch_Account_Info').distinct():
		threads.append(Fetch_Twitter_Account(twitter_id=acc.twitter_id, screen_name=acc, lock=Lock, queue=queue, action="GET_FAVORITES", model="SocialProfile"))
	

	for acc in SocialProfile.objects.filter().exclude(job_status="Fetch_Account_Info").distinct():
		threads.append(Fetch_Twitter_Account(screen_name=acc, twitter_id=acc.twitter_id, lock=Lock, queue=queue, action="Check_Ratio"))
	
	for thread in threads:
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer:
			threads.remove(executer)
		else:
			threads[:] = [t for t in threads]


