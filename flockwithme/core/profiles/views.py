from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from flockwithme.app.scheduler.models import Hashtag, Location, Influencer, TwitterList, TwitterUser, Job
from flockwithme.app.scheduler.forms import HashtagForm, LocationForm, InfluencerForm
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
	if request:
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

	if request.POST:
		form = HashtagForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Hashtags updated!")
		else:
			messages.error(request, "Something went wrong!")
			print form.errors


def my_locations(request):
	if request:
		try:
			accounts = request.user.account.all()
			pk = accounts[0].id
			return render(request, 'my_locations.jade', {
				'locations': ','.join([x.name for x in request.user.locations.all()]),
				'all_locations': json.dumps([x.name for x in Location.objects.filter(profiles__isnull=False)])
				})
		except Exception, e:
			messages.error(request, "Please add a Twitter Account First")
			return redirect("my_accounts")
	
	if request.POST:
		form = LocationForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Locations updated!")
		else:
			messages.error(request, "Uh Oh. Something went wrong on our end. Feel free to harrass Jon.")
			print form.errors


def my_influencers(request):
	if request:
		try:
			accounts = request.user.accounts.all()
			pk=accounts[0].id
		 	return render(request, 'influencers.jade', { 'influencers': ','.join([x.screen_name for x in request.user.influencers.all()]),
			'all_influencers': json.dumps([x.screen_name for x in Influencer.objects.filter(profiles__isnull=False)])
			})
		except Exception, e:
			messages.error(request, "Please add a Twitter Account First.")
			return redirect("my_accounts")
	if request.POST:
		form = InfluencerForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Influencers updated")
		else:
			messages.error(request, "Uh oh, something went wrong on our end. Feel free to harrass Jon.")
	

def my_lists(request):
	if request:
		try:
			accounts = request.user.accounts.all()
			pk=accounts[0].id
			account = request.user.accounts.get(pk=pk)
			token = account.token
			secret = account.secret
		except Exception, e:
			messages.error(request, "Please add a twitter account first.")
			return redirect("my_accounts")
		
	if request.POST:
		owner = request.POST["TwitterListOwner"].split(',')
		should_add = [x for x in owner if x not in TwitterList.objects.filter(profile=request.user)]
		should_delete = [x for x in TwitterList.objects.filter(profile=request.user) if x not in owner]
		
		for i in should_delete:
			if i:
				try:
					i.delete()
				except Exception, e:
					messages.error(request,"Something went wrong trying to delete list owner")
		
		for i in should_add:
			if i:
				try:
					consumer_key, consumer_secret, twitter_key, twitter_secret = token, secret, settings.TWITTER_KEY, settings.TWITTER_SECRET
					auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
					auth.set_access_token(token, secret)
					api = tweepy.API(auth)
					Twitter_User_Id = api.get_user(screen_name = i).id
					Twitter_user, created = TwitterUser.objects.get_or_create(screen_name = i, twitter_id = Twitter_User_Id)
					Twitter_List, created = TwitterList.objects.get_or_create(profile=request.user, name="TBD", owner=Twitter_user)
					accounts = request.user.accounts.all()
					account = accounts[0].id
					job, created = Job.objects.get_or_create(socialprofile_id=account, action="GET_LISTS", twitter_list=Twitter_List)
				except Exception, e:
					print e
		messages.success(request, "list owners updated successfully")


		#form = TwitterListOwnerForm(request.user, request.POST)
		#if form.is_valid():
			#form.save()
			#messages.success(request, "lists updated")
		#else:
			#messages.error(request, "Uh Oh, Something went wrong on our end. Feel free to bug Jon. :D")
			#print form.errors
	return render(request, 'my_lists.jade', {'list_owner':','.join([str(x.owner) for x in TwitterList.objects.filter(profile=request.user)]),
		'all_list_owners': json.dumps([x.name for x in TwitterList.objects.all()]), "twitter_lists":TwitterList.objects.filter(profile=request.user)})

def logout_view(request):
	logout(request)
	return redirect(reverse('landingpage'))
