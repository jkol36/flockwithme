import os
import sys
import time
import tweepy
from optparse import OptionParser

#executes jobs based on their action
class jobsmasher(object):
	def __init__(self, *args, **kwargs):
		self.job = kwargs.pop('job')
		self.action = kwargs.pop('action')
		self.account = kwargs.pop('account')
		try:
			if self.action == "TRACK_FOLLOWERS": 
				print self.job
		except Exception, e:
			print e
		return super(jobsmasher, self).__init__(*args, **kwargs)

	def hello(self):
		print self.job



#constantly pings the database in search for new jobs to execute
class Worker:

	def sleep(n):
		time.sleep(n)


	def execute(self):
		Jobs = Job.objects.filter(is_complete=False)
		if not Jobs:
			self.sleep(20)
		else:
			for job in Jobs:
				jobsmasher(account=job.socialprofile, action=job.action, job=job)
				



if __name__ == '__main__':
	usage = "usage: %prog -s PATH | --path=PATH"
	parser = OptionParser(usage)
	parser.add_option('-s', '--path', dest='path', metavar='PATH', help="The path to the Django environment")
	(options, args) = parser.parse_args()
	if not options.path:
		parser.error("Specify the path where manage.py is")
 
	os.environ['DJANGO_SETTINGS_MODULE'] = "flockwithme.settings"
	sys.path.append(options.path)

	from flockwithme.app.scheduler.models import Job
	from django.core.wsgi import get_wsgi_application
	application = get_wsgi_application()
	from django.conf import settings

	a = Worker()
	a.execute()
