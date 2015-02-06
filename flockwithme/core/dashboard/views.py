from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def index(request):
	new_followers, days, potential_customers, tweets_favorited = 0, 0, 0, 0
	now = timezone.now()
	favorited_tweets = []
	friends_ = []
	for acc in request.user.accounts.all():
		new_followers += acc.get_followers(socialProfile=acc).count()
		potential_customers += (acc.get_friends().count() + acc.get_favorites().count())
		days += ( now - acc.profile.date_joined).days
		tweets_favorited += (acc.get_favorites().count())
		favorites = acc.get_favorites()[:30]
		friends = acc.get_friends()[:30]
		for i in favorites:
			favorited_tweets.append(i)
		for i in friends:
			if i.twitterUser.screen_name != None:
				friends_.append(i.twitterUser.screen_name)
			else:
				pass
	money_saved = 100 * days
	return render(request, 'dashboard.jade', {
		'new_followers': new_followers, 
		'potential_customers': potential_customers,
		'money_saved': money_saved,
		'favorites':favorited_tweets,
		'friends':friends_,
		'tweets_favorited':tweets_favorited,
		})
@login_required

def help(request):
	return render(request, 'help.jade')
