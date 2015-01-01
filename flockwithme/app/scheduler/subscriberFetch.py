import os
import time
import sys
import tweepy
from optparse import OptionParser

class subscriberFetcher(object):
	def __init__(self, *args, **kwargs):
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
			#these are ids so need to fetch the twitterlist object later using the matching id
			twitterlists = [x.twitter_id for x in TwitterList.objects.filter(is_queried=False).distinct()]
			fetch = subscriberFetcher(TwitterLists=twitterlists)
			if not twitterlists:
				time.sleep(20)
			try:
				for tlist in twitterlists:
					api = tweepy.API(self.auth)
					list_members = [x for x in api.list_members(list_id = tlist)]
					tuser_dbase_ids = [x.twitter_id for x in TwitterUser.objects.all()]
					for member in list_members:
						if member.id not in tuser_dbase_ids:
							tuser, created = TwitterUser.objects.get_or_create(screen_name= member.screen_name, followers_count = member.followers_count, location=member.location, friends_count = member.friends_count)
							tuser.save()
							tlist_object = TwitterList.objects.get(twitter_id=tlist)
							tlist_object.is_queried = True
							new_trelationship = TwitterRelationship.objects.create(action="SUBSCRIBE", twitterList=tlist_object)
							tlist.save()
							#add twitter user as a subscriber
							tuser.twitterrelationship_set.add(new_trelationship, 'SUBSCRIBE')
							new_trelationship.save()
							tuser.save()
						elif member.id in tuser_dbase_ids:
							#use the id to fetch twitter user object
							tuser = TwitterUser.objects.get(twitter_id=member.id)
							tlist_object = TwitterList.objects.get(twitter_id=tlist)
							tlist_object.is_queried = True
							new_trelationship = TwitterRelationship.objects.create(action="SUBSCRIBE", twitterList=tlist_object)
							tlist_object.save()
							new_trelationship.save()
							tuser.twitterrelationship_set.add(new_trelationship, 'SUBSCRIBE')
							tuser.save()
					tlist.is_queried = True
					tlist.save()
				self.fetch()
			except Exception, e:
				self.handle_error(e)
	
	def handle_error(self, e):
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

	from flockwithme.app.scheduler.models import TwitterUser, TwitterList, TwitterRelationship
	from django.core.wsgi import get_wsgi_application
	application = get_wsgi_application()

	a = Worker()
	a.fetch()
