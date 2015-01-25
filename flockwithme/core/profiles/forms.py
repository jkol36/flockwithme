from django import forms
from .models import SocialProfile, Profile
from flockwithme.app.scheduler.models import Job
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from flockwithme.app.scheduler.Fetcher import Fetch_Twitter_Account


class ProfileCreationForm(UserCreationForm):
	name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Full Name'}))
	email = forms.EmailField(required=True)
	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password again'}))
 
	class Meta:
		fields = ['email', 'username', 'password1', 'password2']
		model = Profile

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			Profile.objects.get(username=username)
		except Profile.DoesNotExist:
			return username
		raise forms.ValidationError('Username already exists.')
	def clean_password(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_date['password2']
		if password1 != password2:
			raise forms.ValidationError("Password's do not match.")
		else:
			pass	
	def save(self, *args, **kwargs):
		profile = super(ProfileCreationForm, self).save(*args, **kwargs)
		name = self.cleaned_data.get('name').split(' ', 1)
		profile.first_name = name[0]
		profile.last_name = name[1] if len(name) > 1 else ''
		profile.save()
		return profile


class SocialProfileCreationForm(forms.ModelForm):
	provider = forms.CharField(required=True)
	token = forms.CharField(required=True)
	secret = forms.CharField(required=True)
	handle = forms.CharField(required=True)
	class Meta:
		model = SocialProfile
		fields = ['provider', 'token', 'secret', 'handle']


	def __init__(self, profile, *args, **kwargs):
		self.profile = profile
		return super(SocialProfileCreationForm, self).__init__(*args, **kwargs)

	def is_valid(self):
		valid = super(SocialProfileCreationForm, self).is_valid()
		if not valid:
			return valid
		
		if SocialProfile.objects.filter(profile=self.profile, handle=self.cleaned_data.get('handle'), provider=self.cleaned_data.get('provider')).count() > 0:
			return False
		return True



	def save(self, *args, **kwargs):
		#kwargs['commit'] = False
		socialprofile = super(SocialProfileCreationForm, self).save(*args, **kwargs)
		return socialprofile
		#socialprofile.profile = self.profile
		#socialprofile.profile_status = 'pending'
		#socialprofile.followers_count = Fetch_Twitter_Account(screen_name=self.cleaned_data['handle'], action='get_follower_count', model='SocialProfile').get_follower_count()
		#socialprofile.friend_count = Fetch_Twitter_Account(screen_name = self.cleaned_data['handle'], action="get_friend_count", model="SocialProfile").get_friend_count()
		#socialprofile.twitter_id = Fetch_Twitter_Account(screen_name=self.cleaned_data['handle'], action='get_twitter_id', model='SocialProfile').get_twitter_id()
		#socialprofile.save()
		#return socialprofile


class ContactForm(forms.ModelForm):
	pass
