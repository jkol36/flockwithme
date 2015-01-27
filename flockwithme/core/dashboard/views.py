from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def index(request):
	new_followers, days, potential_customers = 0, 0, 0
	now = timezone.now()
	for acc in request.user.accounts.all():
		new_followers += acc.get_initial_followers().count()
		potential_customers += (acc.get_friends().count() + acc.get_favorites().count())
		days += ( now - acc.profile.date_joined).days
	money_saved = 100 * days
	return render(request, 'dashboard.jade', {
		'new_followers': new_followers, 
		'potential_customers': potential_customers,
		'money_saved': money_saved
		})
@login_required

def help(request):
	return render(request, 'help.jade')
