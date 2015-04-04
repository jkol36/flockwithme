# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
import tweepy
from .models import Hashtag, Location, Job, Influencer, TwitterList, TwitterUser, TwitterListOwner
from geopy import GoogleV3
from flockwithme.core.profiles.models import SocialProfile, Profile
import logging

#Called in scheduler/views

class StartForm(object):

	def __init__(self, profile, *args, **kwargs):
		self.profile = profile
		print self.profile
		return super(StartForm, self).__init__()

	def save(self):
		social_profiles = SocialProfile.objects.filter(profile=self.profile)
		for t_account in social_profiles:
			self.start(t_account)

	def start(self, t_account):
		hashtags = [x for x in Hashtag.objects.filter(profile=self.profile)]
		return Job.objects.get_or_create(
			   social_profile=t_account, 
			   hashtags=hashtags)





class HashtagForm(forms.Form):
	hashtags = forms.CharField(required=False)

	def __init__(self, profile, *args, **kwargs):
		self.profile = profile
		return super(HashtagForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		my_hashtags = [h.name for h in self.profile.hashtags.all()]
		hashtags = self.cleaned_data.get('hashtags').split(',')
		should_delete = [x for x in my_hashtags if x not in hashtags]
		should_add = [x for x in hashtags if x not in my_hashtags]
		for name in should_add:
			if name:
				hashtag, _ = Hashtag.objects.get_or_create(name=name.lstrip('#').lower())
				hashtag.profiles.add(self.profile)
				hashtag.save()
		for name in should_delete:
			if name:
				hashtag, _ = Hashtag.objects.get_or_create(name=name.lstrip('#').lower())
				self.profile.hashtags.remove(hashtag)
		self.profile.save()

class InfluencerForm(forms.Form):
	influencers = forms.CharField(required=False)

	def __init__(self, profile, *args, **kwargs):
		self.profile = profile
		return super(InfluencerForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		my_influencers = [h.screen_name for h in self.profile.influencers.all()]
		influencers = self.cleaned_data.get('influencers').split(',')
		should_delete = [x for x in my_influencers if x not in influencers]
		should_add = [x for x in influencers if x not in my_influencers]
		for screen_name in should_add:
			if screen_name:
				influencer, _ = Influencer.objects.get_or_create(screen_name=screen_name.lstrip('@').lower())
				influencer.profiles.add(self.profile)
				influencer.save()
		for screen_name in should_delete:
			if screen_name:
				influencer, _ = Influencer.objects.get_or_create(screen_name = screen_name.lstrip('@').lower())
				self.profile.influencers.remove(influencer)
		self.profile.save()


class TwitterListForm(forms.Form):
	#get the list owners submitted
	list_owner = forms.CharField(required = False)

	def __init__(self, profile, *args, **kwargs):
		self.profile = profile
		return super(TwitterListForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		my_owners = [x.screen_name for x in self.profile.owners.all()]
		submitted_list_owners = self.cleaned_data.get('list_owner').split(',')
		should_delete = [x for x in my_owners if x not in submitted_list_owners]
		should_add = [x for x in submitted_list_owners if x not in my_owners]
		for name in should_add:
			owner, _ = TwitterListOwner.objects.get_or_create(screen_name=name)
			owner.save
			self.profile.owners.add(owner)
		for name in should_delete:
			if name:
				owner, _ = TwitterListOwner.objects.get_or_create(screen_name=name)
				owner.save()
				self.profile.owners.remove(owner)
		self.profile.save()
		




class LocationForm(forms.Form):
	locations = forms.CharField(required=False)

	def __init__(self, profile, *args, **kwargs):
		 self.profile = profile
		 return super(LocationForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		my_locations = [l.name for l in self.profile.locations.all()]
		locations = self.cleaned_data.get('locations').split(',')
		should_delete = [x for x in my_locations if x not in locations]
		should_add = [x for x in locations if x not in my_locations]
		geolocator = None
		for name in should_add:
			if name:
				loc, created = Location.objects.get_or_create(name=name.lower())
				if created:
					if not geolocator:
						geolocator = GoogleV3()
					address, (la, lo) = geolocator.geocode(name)
					loc.latitude = la
					loc.longitude = lo
				loc.profiles.add(self.profile)
				loc.save()
		for name in should_delete:
			if name:
				loc, _ = Location.objects.get_or_create(name=name.lower())
				self.profile.locations.remove(loc)
		self.profile.save()

			

			

				
	


	



		