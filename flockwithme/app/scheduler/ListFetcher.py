import os
import sys
import tweepy
import time
from optparse import OptionParser



class listFetcher(object)
	def __init__(self, TwitterListOwners):
		self.TwitterListOwners = TwitterListOwners
		self.checker = time.time()
		return super(listFetcher, self).__init__(self, TwitterListOwners)

	


class Worker:
	def __init__(self):
		apikey = 'moX6M9jbbIuAnYuaAxZJFkzQY'
		apisecret = 'YhH1Fgr4VUyzLsKoKKQrR0bRuPbsqP4daiiZ9UbbSyZWDCsTxU'
		access_token = '1177046514-QVUDUBANp0p2HHiJrBJIwYXyaqjZkQg7NMHSRwA'
		access_secret = 'gBDQ3Z2wNGMOptyAsLffOHksIbhYlL6RvbCYSHzkWV08s'
		self.auth = tweepy.OAuthHandler(apikey, apisecret)
		self.auth.set_access_token(access_token, access_secret)

	def Fetch(self):
		while 1:
			owners = TwitterListOwners.objects.filter(is_queried=False).distinct()
			if not owners:
				time.sleep(20)
			print owners


	




if __name__ == "__main__":
	usage = "usage: %prog -s PATH | --path=PATH"
	parser = OptionParser(usage)
	parser.add_option('-s', '--path', dest='path', metavar='PATH', help="The path to the django environment")
	(options, args) = parser.parse_args()
	if not options.path:
		parser.error("Specify the path where manage.py is.")
	os.environ['DJANGO_SETTINGS_MODULE'] = "flockwithme.settings"
	sys.path.append(options.path)

	#######################################
	from flockwithme.app.scheduler.models import TwitterListOwner
	a = Worker()
	a.Fetch()

