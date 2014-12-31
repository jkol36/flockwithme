import os
import sys
import tweepy
import time
from optparse import OptionParser



class listFetcher(object):
	def __init__(self, TLOWNERS, *args, **kwargs):
		self.TLOWNERS = kwargs.pop("TwitterListOwners")
		self.checker = time.time()
		return super(listFetcher, self).__init__(*args, **kwargs)
	


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
			#submitted twitter list owners that haven't been querried yet
			owners = [x.screen_name for x in TwitterListOwner.objects.filter(is_queried=False).distinct()]
			#Instantiate our listFetcher class
			fetch = listFetcher(self, TwitterListOwners=owners)
			if not owners:
				#if there aren't twitter owners then sleep
				time.sleep(20)
			#if there are newly added twitterlistowners	
			for i in owners:
				try:
					#each twitter list owner will need to have a relationship with TwitterUser so we can give them a following count, favorite_count, etc
					tusers = [x.screen_name for x in TwitterUser.objects.all()]
					# if the owner is not a twitter user instance
					if i not in tusers:
						#lookup the owners twitter profile using the twitter api
						tobject = self.lookup_user(owner=i)
						#create a new twitter user instance with the information
						new_twitter_user, _ = TwitterUser.objects.get_or_create(screen_name=tobject['screen_name'], twitter_id=tobject['twitter_id'], followers_count=tobject['follower_count'], friends_count=tobject['friends_count'], location=tobject['location'])
						#save the twitter user instance
						new_twitter_user.save()
						#use the twitter api to fetch the users lists using the screen_name inputted for lookup
						all_lists = self.get_lists(owner=i)
						#Update the list_owner object so he now has a ForeignKey relationship with the twitter user instance
						tlistowner_twitter_profile = TwitterListOwner.objects.filter(screen_name=i).update(twitter_profile=new_twitter_user)
						#Get the twitter list owner from the database using the screen_name for lookup
						tlistowner = TwitterListOwner.objects.get(screen_name=i)
						tlistowner.is_queried = True
						tlistowner.save()
						all_lists = self.get_lists(owner=i)
						if len(all_lists)> 0:
							tlistowner.owns_list = True
							tlistowner.save
							tuser.has_lists = True
							tuser.save()
							for l in all_lists:
								ctlist = self.add_lists_to_database(tlist=l, owner=tlistowner)


					#if the screen_name is already in our database
					else:
						#Get the twitter user instance using the screen_name
						tuser = TwitterUser.objects.get(screen_name=i)
						#Add the twitter user as a foreign key to the twitter list owner
						tlistowner_twitter_profile = TwitterListOwner.objects.filter(screen_name=i).update(twitter_profile=tuser)
						#get the twitter list owner using the screen_name
						tlistowner = TwitterListOwner.objects.get(screen_name=i)
						#Mark the Twitter list owner as querried
						tlistowner.is_queried = True
						#save the list owner
						tlistowner.save()
						#Get all the lists associated with the screen_name
						all_lists = self.get_lists(owner=i)
						#if the len of all lists is greater than one, this screen_name (twitter list owner and twitter user has lists.) Otherwise, he doesn't.
						if len(all_lists) > 0:
							tlistowner.owns_list = True
							tuser.has_lists = True
							tlistowner.save()
							for l in all_lists:
								ctlist = self.add_lists_to_database(tlist=l, owner=tlistowner)
				except Exception, e:
					self.handle_error(e)	

						

					
					
	def handle_error(self, e):
		#page does not exist error
		if e.args[0][0]['code'] == 34:
			 pass
		elif e.args[0][0]['code'] == 88:
			return time.sleep(20)


	def get_lists(self, owner):
		api = tweepy.API(self.auth)
		all_lists = api.lists_all(owner)
		return all_lists

	def add_lists_to_database(self, tlist, owner):
		twitter_id = tlist.id
		name = tlist.name
		tlist, created = TwitterList.objects.get_or_create(name=name, twitter_id=twitter_id, owner=owner)
		tlist.save()
		return tlist



	#twitter lookup
	def lookup_user(self, owner):
		api = tweepy.API(self.auth)
		user = api.get_user(screen_name=owner)
		return {'screen_name':owner, 'twitter_id':user.id, 'location': user.location, 'friends_count':user.friends_count, 'follower_count':user.followers_count}


	

			


	




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
	from flockwithme.app.scheduler.models import TwitterListOwner, TwitterUser, TwitterList
	from django.core.wsgi import get_wsgi_application
	application = get_wsgi_application()
	a = Worker()
	a.Fetch()

