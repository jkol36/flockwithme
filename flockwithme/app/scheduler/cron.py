import kronos
from flockwithme.core.profiles.models import Profile, SocialProfile
from .jobexecuter import JobExecuter
from .accountfetch import AccountFetch
from Queue import Queue
from threading import Lock
from django.db.models import Q


@kronos.register('0 3 * * *')
def do_work():
	queue = Queue()
	threads = []
	passive_jobs = []
	for acc in SocialProfile.objects.filter(jobs__isnull=False).distinct():
		jobs = acc.jobs.all().exclude(Q(action="TRACK_FOLLOWERS") | Q(action="AUTO_DM") | Q(action="GET_LISTS") | Q(action="GET_LIST_SUBSCRIBERS") | Q(action="GET_ACCOUNT_INFO") |Q(action="GET_FOLLOWERS"))
		threads.append(JobExecuter(account=acc, queue=queue, jobs=jobs))

	for thread in threads:
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

@kronos.register('0 6 * * *')
def fetch_account_info():
	queue = Queue()
	threads = []

	for acc in SocialProfile.objects.filter(jobs__isnull=False).distinct():
		jobs = acc.jobs.filter(Q(action="GET_ACCOUNT_INFO"))
		if jobs:
			threads.append(AccountFetch(lock = Lock, account=acc, queue=queue, jobs=jobs))
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
			threads[:] = [t for t in threads]

