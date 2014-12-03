from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

from flockwithme.app.scheduler.models import Hashtag, Location, Influencer, TwitterList
from flockwithme.app.scheduler.forms import HashtagForm, LocationForm, InfluencerForm, TwitterListOwnerForm
from django.contrib import messages
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

	return render(request, 'my_hashtags.jade', {
		'hashtags': ','.join([x.name for x in request.user.hashtags.all()]),
		'all_hashtags': json.dumps([x.name for x in Hashtag.objects.all()[:20]])
		})

def my_locations(request):
	if request.POST:
		form = LocationForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Locations updated!")
		else:
			messages.error(request, "Uh Oh. Something went wrong on our end. Feel free to harrass Jon.")
			print form.errors

	return render(request, 'my_locations.jade', {
		'locations': ','.join([x.name for x in request.user.locations.all()]),
		'all_locations': json.dumps([x.name for x in Location.objects.filter(profiles__isnull=False)])
		})

def my_influencers(request):
	if request.POST:
		form = InfluencerForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Influencers updated")
		else:
			messages.error(request, "Uh oh, something went wrong on our end. Feel free to harrass Jon.")
	return render(request, 'influencers.jade', { 'influencers': ','.join([x.screen_name for x in request.user.influencers.all()]),
		'all_influencers': json.dumps([x.screen_name for x in Influencer.objects.filter(profiles__isnull=False)])
		})

def my_lists(request):
	accounts = request.user.accounts.all()
	pk=accounts[0].id
	account = request.user.accounts.get(pk=pk)
	token = account.token
	secret = account.secret
	if request.POST:
		print request.POST
		form = TwitterListOwnerForm(request.user, request.POST, token, secret)
		if form.is_valid():
			form.save()
			messages.success(request, "lists updated")
		else:
			messages.error(request, "Uh Oh, Something went wrong on our end. Feel free to bug Jon. :D")
			print form.errors
	return render(request, 'my_lists.jade', {'list_owner':','.join([x.owner for x in TwitterList.objects.all()]),
		'all_list_owners': json.dumps([x.owner for x in TwitterList.objects.all()])})

def logout_view(request):
	logout(request)
	return redirect(reverse('landingpage'))
