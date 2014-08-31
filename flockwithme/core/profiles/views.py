from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from flockwithme.app.scheduler.models import Hashtag, Location, Influencer #Lists
from flockwithme.app.scheduler.forms import HashtagForm, LocationForm, InfluencerForm #follow_members_of_list_form
from django.contrib import messages
import json

def my_accounts(request):
	return render(request, 'my_accounts.jade')

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
'''
def my_lists(request):
	if request.POST:
		form = follow_members_of_list_form(request.user, request.POST)
		if form_is_valid():
			form.save()
			messages.success(request, "lists updated")
		else:
			messages.error(request, "Uh Oh, Something went wrong on our end. Feel free to bug Jon. :D")
			print form.errors
	return render(request, 'my_lists.jade', {
		'lists': ','.join([x.name for x in request.user.lists.all()]),
		'all_lists': json.dumps([x.name for x in Lists.objects.filter(profiles__isnull = False)])
		})
'''
def logout_view(request):
	logout(request)
	return redirect(reverse('landingpage'))
