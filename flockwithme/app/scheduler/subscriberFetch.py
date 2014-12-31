import os
import time
import sys
import tweepy
from optParse import OptionParser

class subscriberFetcher(object):
	def __init__(self, twitterlists, *args, **kwargs):
		self.twitterlists = kwargs.pop('TwitterLists')
		return super(subscriberFetcher, self).__init__(*args, **kwargs)


class Worker:
	def __init__(self):
		apikey = 'moX6M9jbbIuAnYuaAxZJFkzQY'
		apisecret = 'YhH1Fgr4VUyzLsKoKKQrR0bRuPbsqP4daiiZ9UbbSyZWDCsTxU'
		access_token = '1177046514-QVUDUBANp0p2HHiJrBJIwYXyaqjZkQg7NMHSRwA'
		access_secret = 'gBDQ3Z2wNGMOptyAsLffOHksIbhYlL6RvbCYSHzkWV08s'
		self.auth = tweepy.OAuthHandler(apikey, apisecret)
		self.auth.set_access_token(access_token, access_secret)


	def fetch(self):
		while 1:
			twitterlists = [x.id for x in TwitterList.objects.filter(is_queried=False).distinct()]
			fetch = subscriberFetcher(TwitterLists=twitterlists)
			if not twitterlists:
				time.sleep(20)
			try:
				for tlist in twitterlists:
					api = tweepy.api(self.auth)
					list_members = [x for x in api.list_members(list_id = tlist)]
					for member in list_members:
						tuser, created = TwitterUser.objects.get_or_create(screen_name= x.screen_name, followers_count = x.followers_count, location=x.location, friends_count = x.friends_count)
						tuser.save()
						tlist.subscribers.add(tuser)
						tlist.subscribers.save()
						tlist.save()
				self.fetch()
			except Exception, e:
				self.handle_error(e)
	
	def handle_error(self, e):
		if e.args[0][0]['code'] == 34:
			pass
		elif e.args[0][0]['code'] == 88:
			time.sleep(20)
		else:
			print e

	if __name__ == "__main__":
		usage = 'usage: %prog -s PATH | --path=PATH'
		parser = OptionParser(usage)
		parser.add_option('-s', '--path', dest='path', metavar='PATH', help="The path to the django environment")
		(options, args) = parser.parse_args()
		if not options.path:
			parser.error("Specify the path where manage.py is.")
		os.environ['DJANGO_SETTINGS_MODULE'] = "flockwithme.settings"
		sys.path.append(options.path)

		from flockwithme.app.scheduler.models import TwitterUser, TwitterList
		from django.core.wsgi import get_wsgi_application
		application = get_wsgi_application()

		a = Worker()
		a.fetch()
