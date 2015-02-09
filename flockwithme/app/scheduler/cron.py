import kronos
from flockwithme.core.profiles.models import Profile, SocialProfile
from flockwithme.app.scheduler.models import Influencer, ApiStatus, Job
from .jobexecuter import JobExecuter
from .accountfetch import AccountFetch
from .Fetcher import FetchInfluencerInfo, FetchSocialProfileInfo
from Queue import Queue
from threading import Lock
from django.db.models import Q
from .auto_pilot import AutoPilot, OnTweet, OnUnfinishedJob, OnRatioDirty
from .oauthtest import TestApi



"""@kronos.register('0 10 * * *')
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

#test kronos
@kronos.register('* * * * *')
def testkronos():
	queue = Queue()
	threads = []
	threads.append(FetchSocialProfileInfo(queue = queue, action = "Test", socialprofile=SocialProfile.objects.get(handle="Jkol36")))
	for thread in threads:
		thread.start()


#Once every 24 hours change social profiles from rate limited to not rate limited

@kronos.register('* * * * * ')
def SetLimitsFalse():
	queue = Queue()
	for acc in SocialProfile.objects.filter(Q(follow_limit_reached=True) | Q(favorite_limit_reached=True)):
		acc.follow_limit_reached = False
		acc.favorite_limit_reached = False
		acc.save()


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

"""
"""
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
"""
"""
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
#every 2 minutes check database api status
#if api status is limited then check to see if it has requests left.
@kronos.register('*/2 * * * *')
def check_api_status():
	apistatus = ApiStatus.objects.filter(status="Rate_Limited")[0]
	if apistatus:
		requests_left = TestApi().get_remaining_follow_requests()
		if requests_left > 1:
			apistatus.status = "Active"
			apistatus.save()

@kronos.register('* * * * *')
def test_fav():
	print TestApi().favorite_tweets()
"""
############# FETCHING JOBS ########################
#Every 30 minutes check for new accounts. Fetch their followers, friends, and favorites.
@kronos.register('*/30 * * * *')
def FetchSocialProfileInitial():
	queue = Queue()
	threads = []
	lock = Lock()
	
	for acc in SocialProfile.objects.filter(new_account=True):
		threads.append(FetchSocialProfileInfo(socialprofile=acc, is_initial=True, query_twitter = True, queue=queue, action="Get_Everything"))

	for thread in threads:
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer != None:
			print 'executer needs to bre removied'
			threads.remove(executer)
		else:
			threads[:] = [t for t in threads if t.isAlive()]
#update favorites, followers, freinds, etc
#every 2 hours get everything
@kronos.register('* * * * *')
def FetchSocialProfile():
	queue = Queue()
	threads = []
	lock = Lock()
	
	for acc in SocialProfile.objects.filter(new_account=False):
		threads.append(FetchSocialProfileInfo(is_initial=False, query_twitter=False, socialprofile=acc, queue=queue, action="Get_Everything"))
	for thread in threads:
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer != None:
			print 'executer needs to bre removied'
			threads.remove(executer)
		else:
			threads[:] = [t for t in threads if t.isAlive()]



#fetch twitter follower count, friend count and twitter_id for new profiles
@kronos.register('0/25 * * * *')
#NEW ACCOUNT
#RUN EVERY 25 MINUTES
#FETCH TWITTER ID, FOLLOWER_COUNT, FRIEND_COUNT, TWEET_COUNT
def New_Account():
	queue =Queue()
	threads = []
	lock = Lock()
	for acc in SocialProfile.objects.filter(new_account=True):
		threads.append(FetchSocialProfileInfo(action="NEW_ACCOUNT", queue=queue, socialprofile=acc))

	for thread in threads:
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer != None:
			threads._Thread.delete()
		else:
			threads[:] = [t for t in threads if t.isAlive()]


#every 10 minutes check for new tweets



############################# ACTION JOBS ##############################
@kronos.register('*/10 * * * *')
def TrackSocialProfileTweets():
	queue = Queue()
	lock = Lock()
	threads = []
	apistatus = ApiStatus.objects.all()[0].status
	
	for acc in SocialProfile.objects.filter(is_initial=False):
		threads.append(FetchSocialProfileInfo(is_initial=False, queue=queue, query_twitter=False, socialprofile=acc, action="Get_Tweet_Count"))

	for thread in threads:
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer != None:
			print 'executer needs to bre removied'
			threads.remove(executer)
		else:
			threads[:] = [t for t in threads if t.isAlive()]

@kronos.register('*/5 * * * *')
def TrackSocialProfile():
	queue = Queue()
	threads = []
	for acc in SocialProfile.objects.filter(new_account=False):
		threads.append(FetchSocialProfileInfo(is_initial=False, queue=queue, query_twitter=False, socialprofile=acc, action="Get_Count"))
@kronos.register('* 23 * * *')
def CleanSocialProfile():
	queue = Queue()
	threads = []
	for acc in SocialProfile.objects.filter(is_clean=False).exclude(new_account=True):
		threads.append(OnRatioDirty(socialprofile=acc, queue=queue))

	for thread in threads:
		thread.start()

	while threads:
		try:
			executer = queue.get(timeout=1)
		except:
			executer = None
		if executer != None:
			threads.remove(executer)



"""
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
"""
