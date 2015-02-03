import kronos
from flockwithme.core.profiles.models import Profile, SocialProfile
from flockwithme.app.scheduler.models import Influencer
from .jobexecuter import JobExecuter
from .accountfetch import AccountFetch
from .Fetcher import FetchInfluencerInfo, FetchSocialProfileInfo
from Queue import Queue
from threading import Lock
from django.db.models import Q
from .auto_pilot import AutoPilot



@kronos.register('0 10 * * *')
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

@kronos.register('* * * * *')
def track_social_profile():
	queue = Queue()
	threads = []
	for socialprofile in SocialProfile.objects.all():
		threads.append(FetchSocialProfileInfo(socialprofile=socialprofile, action="Get_Tweets", queue=queue))

	for thread in threads:
		thread.start()
@kronos.register('*/5 * * * *')
def Fetch_Influencer_Followers():
	queue = Queue()
	threads = []

	for influencer in Influencer.objects.filter(been_queried=False):
		threads.append(Fetch_Influencers_Followers(influencer=influencer, screen_name=influencer.screen_name, queue=queue))
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

@kronos.register('* * * * *')
def FetchSocialProfileInitial():
	queue = Queue()
	threads = []
	for acc in SocialProfile.objects.filter(is_initial=True):
		threads.append(FetchSocialProfileInfo(socialprofile=acc, is_initial=True, queue=queue, action="Get_Everything"))

	for thread in threads:
		thread.start()
@kronos.register('* * * * *')
def FetchSocialProfile():
	queue = Queue()
	threads = []
	for acc in socialprofile.objects.filter(is_initial=False):
		threads.append(FetchSocialProfileInfo(is_initial=False, socialprofile=acc, queue=queue, action="Get_Everything"))
	for thread in threads:
		thread.start()
@kronos.register('* * * * *')
####initial influencer query 
def fetch_influencer_info():
	queue = Queue()
	threads = []
	for influencer in Influencer.objects.filter(been_queried=False):
		threads.append(FetchInfluencerInfo(influencer=influencer, queue=queue, screen_name=influencer.screen_name, is_initial=True, action="Get_Everything"))
	for thread in threads:
		thread.start()
@kronos.register('*/15 * * * *')
def fetch_account_info():
	queue = Queue()
	threads = []

	for acc in SocialProfile.objects.filter(job_status='Fetch_Account_Info').distinct():
		threads.append(Fetch_Account_Info(twitter_id=acc.twitter_id, lock = Lock, queue=queue, action="get_everything"))
		#acc.job_status = 'Fetching_Account_Info'
		#acc.save()

	#for acc in SocialProfile.objects.filter().exclude(job_status='Fetch_Account_Info').distinct():
		#threads.append(Fetch_Account_Info(twitter_id=acc.twitter_id, lock=Lock, queue=queue, action="GET_FAVORITES"))
	

	#for acc in SocialProfile.objects.filter().exclude(job_status="Fetch_Account_Info").distinct():
		#threads.append(Fetch_Twitter_Account(twitter_id=acc.twitter_id, lock=Lock, queue=queue, action="Check_Ratio", model="SocialProfile"))
	
	for thread in threads:
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer != None:
			print 'executer needs to bre removied'
			#threads.remove(executer)
		else:
			threads[:] = [t for t in threads if t.isAlive()]

#@kronos.register('*/15 * * * *')
#def auto_dm_followers():
	#queue = queue()
	#threads = []
	#for acc in SocialProfile.objects.filter(has_dm_message=True):
		#threads.append(AutoPilot())

