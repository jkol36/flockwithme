from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from flockwithme.app.scheduler.models import Hashtag, Location, Influencer, TwitterList, TwitterUser, Job
from flockwithme.app.scheduler.forms import HashtagForm, LocationForm, InfluencerForm, TwitterListForm
from django.contrib import messages
import tweepy
from django.conf import settings
import json

def my_accounts(request):
	return render(request, 'my_accounts.jade')

def help(request):
	return render(request, 'help.jade')

class ContactFormView(FormView):
    form_class = ContactForm

    def form_valid(self, form):
        form.save()
        return super(ContactFormView, self).form_valid(form)

    def get_form_kwargs(self):
        # ContactForm instances require instantiation with an
        # HttpRequest.
        kwargs = super(ContactFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        # This is in a method instead of the success_url attribute
        # because doing it as an attribute would involve a
        # module-level call to reverse(), creating a circular
        # dependency between the URLConf (which imports this module)
        # and this module (which would need to access the URLConf to
        # make the reverse() call).
        return reverse('contact_form_sent')

def my_hashtags(request):
	if request.POST:
		form = HashtagForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Hashtags updated!")
		else:
			messages.error(request, "Something went wrong!")
			print form.errors

	#if request is get. Check to see if the user has authenticated twitter accounts.If he doesn't redirect to my_accounts
	try:
		accounts = request.user.accounts.all()
		pk = accounts[0].id
		return render(request, 'my_hashtags.jade', {
			'hashtags': ','.join([x.name for x in request.user.hashtags.all()]),
			'all_hashtags': json.dumps([x.name for x in Hashtag.objects.all()[:20]])
			})
	except Exception, e:
		messages.error(request, "Please add a Twitter Account First.")
		return redirect("my_accounts")

	


def my_locations(request):
	if request.POST:
		form = LocationForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Locations updated!")
		else:
			messages.error(request, "Uh Oh. Something went wrong on our end. Feel free to harrass Jon.")
			print form.errors


	try:
		accounts = request.user.accounts.all()
		pk = accounts[0].id
		return render(request, 'my_locations.jade', {
			'locations': ','.join([x.name for x in request.user.locations.all()]),
			'all_locations': json.dumps([x.name for x in Location.objects.filter(profiles__isnull=False)])
			})
	except Exception, e:
		print e
		messages.error(request, "Please add a Twitter Account First")
		return redirect("my_accounts")
	
	


def my_influencers(request):
	if request.POST:
		form = InfluencerForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Influencers updated")
		else:
			messages.error(request, "Uh oh, something went wrong on our end. Feel free to harrass Jon.")


	try:
		accounts = request.user.accounts.all()
		pk=accounts[0].id
	 	return render(request, 'influencers.jade', { 'influencers': ','.join([x.screen_name for x in request.user.influencers.all()]),
		'all_influencers': json.dumps([x.screen_name for x in Influencer.objects.filter(profiles__isnull=False)])
		})
	except Exception, e:
		messages.error(request, "Please add a Twitter Account First.")
		return redirect("my_accounts")
	
	
#User adds a list owner and we fetch their lists. Form is handled by TwitterListForm in forms.py
def my_lists(request):
	if request.POST:
		form = TwitterListForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "List Owners Updated")
		else:
			messages.error(request, "Something went wrong")
	try:
		accounts = request.user.accounts.all()
		pk = accounts[0].id
		return render(request, 'my_lists.jade', {'list_owner':','.join(x.screen_name for x in request.user.owners.all())}) 
	except Exception, NoAccounts:
		messages.error(request, "Please add a twitter account first")
		return redirect("my_accounts")
		
#def dont_unfollow(request):
	#if request.POST:
		#form = dont_unfollow_form(request.POST)
		#if form.is_valid():
			#messages.success(request, "Success!!")
			#return render(request, 'dont_unfollow.jade')

		#else:
			#for t, z in form.errors:
				#messages.error(request, t + z.as_text())
			#return render(request, 'dont_unfollow.jade')
	#return render(request, "dont_unfollow.jade")

def logout_view(request):
	logout(request)
	return redirect(reverse('landingpage'))
