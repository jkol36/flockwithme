# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
import tweepy
from .models import Hashtag, Location, Job, Influencer, TwitterList, TwitterUser
from geopy import GoogleV3
from flockwithme.core.profiles.models import SocialProfile, Profile
import logging


class JobCreationForm(forms.Form):
	action = forms.ChoiceField(required=True, choices=Job.ACTION_CHOICES)
	socialProfile = forms.IntegerField(required=True)
	profile = forms.IntegerField(required=True)
	message = forms.CharField(required=False)
	hashtag = forms.IntegerField(required=False)
	influencer = forms.IntegerField(required = False)
	#list_= forms.IntegerField(required = False)
	twitter_username = forms.CharField(required=False)
	location = forms.IntegerField(required=False)
	radius = forms.IntegerField(required=False)

	def clean(self):
		super(JobCreationForm, self).clean()
		try:
			self.cleaned_data['radius'] = int(self.cleaned_data['radius'])
		except:
			self.cleaned_data['radius'] = 0
		self.cleaned_data['location'] = self.cleaned_data['location'] or None
		self.cleaned_data['hashtag'] = self.cleaned_data['hashtag'] or None
		self.cleaned_data['influencer'] = self.cleaned_data['influencer'] or None
		#self.cleaned_data['lists'] = self.cleaned_data['lists'] or None
		return self.cleaned_data


	def is_valid(self):
		valid = super(JobCreationForm, self).is_valid()
		if not valid:
			return valid
		if self.cleaned_data['action'] == "AUTO_DM":
			if not self.cleaned_data['message']:
				self._errors = 'Provide a message'
				return False
		try:
			if self.cleaned_data['hashtag']:
				self.hashtag = Hashtag.objects.get(pk=self.cleaned_data['hashtag'])
			else:
				self.hashtag = None
		except Hashtag.DoesNotExist:
			self._errors = 'There is no such hashtag'
			return False
		try:
			if self.cleaned_data['location']:
				self.location = Location.objects.get(pk=self.cleaned_data.get('location'))
			else:
				self.location = None
		except Location.DoesNotExist:
			self._errors['location'] = "There is no such location"
			return False
		try:
			if self.cleaned_data['influencer']:
				self.influencer = Influencer.objects.get(pk=self.cleaned_data.get('influencer'))
			else:
				self.influencer = None
		except Influencer.DoesNotExist:
			self._errors['influencer'] = "There is no such influencer"
			return False
		'''	
		try: 
			if self.cleaned_data['lists']:
				self.list_name= list_.objects.get(pk=self.cleaned_data.get('lists'))
			else:
				self.list_name = None
		except List_.DoesNotExist:
			self.errors['lists']= 'There is no such list'
		'''	
		try:
			self.profile = Profile.objects.get(pk=self.cleaned_data.get('profile'))
			self.socialProfile = self.profile.accounts.get(pk=self.cleaned_data.get('socialProfile'))
		except Exception:
			self._errors['profile'] = "Something is wrong with profile"
			return False
		return True

	def save(self):
		job = Job(socialprofile=self.socialProfile)
		job.action = self.cleaned_data.get('action')
		job.message = self.cleaned_data.get('message')
		job.hashtag = self.hashtag
		job.influencer = self.influencer
		#job.list = self.lists
		job.location = self.location
		job.radius = self.cleaned_data.get('radius')

		job.save()
		return job




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


class listForm(forms.Form):
	lists = forms.CharField(required = False)

	def __init__(self, profile, *args, **kwargs):
		self.profile = profile
		return super(list_form, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		my_lists = [h.name for h in self.profile.lists.all()]
		lists = self.cleaned_data.get('lists').split(',')
		should_delete = [x for x in my_lists if x not in lists]
		should_add = [x for x in lists if x not in my_lists]
		for name in should_add:
			if name:
				list_, _ = Lists.objects.get_or_create(name = name.lstrip('').lower())
				list_.profiles.add(self.profile)
				list_.save()
		for name in should_delete:
			if name:
				list_, _ = Lists.objects.get_or_create(name = name.lstrip('').lower())
				self.profile.lists.remove(list_)
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

class TwitterListOwnerForm(forms.Form):
	TwitterListOwner = forms.CharField(required = False)

	def __init__(self, profile, token, secret, *args, **kwargs):
		self.profile = profile
		print args
		return super(TwitterListOwnerForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		from jobexecuter import JobExecuter
		logger = logging.getLogger(__name__)
		TwitterListOwners = self.cleaned_data['TwitterListOwner'].split(',')
		should_add = [x for x in TwitterListOwners if x not in TwitterList.objects.filter(pk=self.profile.id)]
		print should_add
		should_delete = [x for x in TwitterList.objects.filter(pk=self.profile.id) if x not in TwitterListOwners]
		print "Should Delete %s" %(should_delete)
		print "Should add %s" %(should_add)
		for name in should_add:
			a,b = (settings.TWITTER_KEY, settings.TWITTER_SECRET)
			#t_id = JobExecuter(screen_name=name, job= queue=None, account=None, jobs=None)
			#create object with t_id as the twitter_id
			

			

				
	


	



		