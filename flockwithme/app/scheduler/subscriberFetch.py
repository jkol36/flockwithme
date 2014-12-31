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
		apikey = 'A85LMuoUZWoIMS5ucFvOJ4Xyi'
		apisecret = 'ZEgb2EqddbEHJWHVpdW0EOwseHSNETHYIsAse3G6KS4NfaePTE'
		access_token = '902679572-s2DiIqemQYrGosdf1btbCsuV6E3prdmtXUYAm985'
		access_secret = 'AoHgOEdyMgpEI1EfW996HMe0XuZkJSCTDX5tcROZLKxYC'
		self.auth = tweepy.OAuthHandler(apikey, apisecret)
		self.auth.set_access_token(access_token, access_secret)


	def fetch(self):
		while 1:
			twitterlist_ids = [x.twitter_id for x in TwitterList.objects.filter(is_queried=False).distinct()]
			fetch = subscriberFetcher(TwitterLists=twitterlist_ids)
			if not twitterlist_ids:
				time.sleep(20)
			try:
				for list_id in twitterlist_ids:
					api = tweepy.API(self.auth)
					list_members = api.list_members(list_id = list_id)
					for member in list_members:
						if member.id not in [x.twitter_id for x in TwitterUser.objects.all()]:
							tuser, created = TwitterUser.objects.get_or_create(screen_name= member.screen_name, twitter_id = member.id, followers_count = member.followers_count, location=member.location, friends_count = member.friends_count)
							tuser.save()
						else:
							tuser = TwitterUser.objects.get(twitter_id=member.id)
						tlist = TwitterList.objects.get(twitter_id=list_id)
						t_relationship, _ = TwitterRelationship.objects.get_or_create(action="SUBSCRIBE", twitterUser=tuser, twitterList=tlist)
						t_relationship_id = t_relationship.id
						t_relationship.save()
						get_relationship = TwitterRelationship.objects.get(pk=t_relationship_id)
						tlist.twitterrelationship_set.add(get_relationship)
						tlist.save()
				self.fetch()
			except Exception, e:
				self.handle_error(e)
	
	def handle_error(self, e):
		if e.args[0][0]['code'] = 34:
			pass
		elif e.args[0][0]['code'] = 88:
			time.sleep(20)
		elif not e.args[0][0]['code']:
			pass

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
