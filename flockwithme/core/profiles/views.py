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
	
def has_lists(twitter_user_instance):
	query = twitter_user_instance

def api(self):
	accounts = self.user.accounts.all()
	pk=accounts[0].id
	account = self.user.accounts.get(pk=pk)
	token = account.token
	print token
	secret = account.secret
	print secret
	consumer_key, consumer_secret, access_key, access_secret = token, secret, settings.TWITTER_KEY, settings.TWITTER_SECRET
	auth = tweepy.OAuthHandler(access_key, access_secret)
	auth.set_access_token(token, secret)
	api = tweepy.API(auth)
	return api

def get_account(self):
	accounts = self.accounts.all()
	account = accounts[0].id
	return account

def get_twitter_user_instance(Screen_Name):
	twitter_user_instance = TwitterUser.objects.get(screen_name=Screen_Name)
	try:
		return twitter_user_instance
	except Exception, e:
		print e
		return None

def get_twitter_list_instance(TwitterUser, *args, **kwargs):
	profile = args.pop['profile']
	if profile:
		print profile
	else:
		twitter_list = TwitterList.objects.filter(owner=TwitterUser)
		if twitter_list:
			return twitter_list
		else:
			return None
def twitter_list_through_profile(Profile):
	twitter_list = TwitterList.objects.filter(profile=Profile)
	if twitter_list:
		return [x.owner for x in twitter_list]
	else:
		return None
def create_twitter_list(name, profile, owner, twitter_id):
	twitter_list = TwitterList.objects.create(name=name, profile=profile, owner=owner, twitter_id = twitter_id)
	return twitter_list

def create_twitter_user(screen_name, twitter_id):
	twitter_user = TwitterUser.objects.create(screen_name=screen_name, twitter_id=twitter_id)
	return twitter_user
def my_lists(request):
	if request:
		try:
			API = api(request)
		except Exception, e:
			messages.error(request, "Please add a twitter account first.")
			return redirect("my_accounts")

	if request.POST:
		owner = request.POST["TwitterListOwner"].split(',')
		try:
			already_added_owners = [x.screen_name for x in twitter_list_through_profile(request.user)]
			should_add = [x for x in owner if x not in already_added_owners]
			should_delete = [x for x in already_added_owners if x not in owner]
			print should_add
			print should_delete
			for i in should_add:
				owner = str(i)
				try:
					owner_ = get_twitter_user_instance(owner)
					if owner_.get_queried() == False:
						Job.objects.create(socialprofile_id=get_account(request.user), action="GET_LISTS", owner=owner_)
					else:
						messages.error(request, "This twitter user does not have any lists:(")
				except Exception, e:
					twitter_id = API.get_user(screen_name=owner).id
					new_owner = create_twitter_user(owner, twitter_id)
					Job.objects.create(socialprofile_id=get_account(request.user), action="GET_LISTS", owner=new_owner)

			for screen_name in should_delete:
				screen_name.delete()
				
		except Exception:
			should_add = [x for x in owner]
			user = request.user
			for i in should_add:
				owner = str(i)
				twitter_id = API.get_user(screen_name=owner).id
				new_owner = create_twitter_user(owner, twitter_id)
				Job.objects.create(socialprofile_id=get_account(user), action="GET_LISTS", owner = new_owner)

		messages.success(request, "list owners updated successfully")
		

	return render(request, 'my_lists.jade', {'list_owner':','.join([str(x.owner) for x in TwitterList.objects.filter(profile=request.user)]),
		'all_list_owners': json.dumps([x.name for x in TwitterList.objects.all()]), "twitter_lists":TwitterList.objects.filter(profile=request.user), 'list_followers': ','.join([str(x.owner) for x in request.user.twitterlist_set.all()])})

def logout_view(request):
	logout(request)
	return redirect(reverse('landingpage'))
