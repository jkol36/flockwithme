from django.test import TestCase
from .forms import ProfileCreationForm, SocialProfileCreationForm
from .models import Profile, SocialProfile

class ProfileTest(TestCase):

	def test_profile_creation_form(self):
		data = {'username': 'test', 'email': 'test@test.no', 'name': 'Martin Skow Roed', 'password1': 'martin'}
		form = ProfileCreationForm(data)
		self.assertTrue(form.is_valid())
		profile = form.save()
		self.assertEqual(profile.first_name, "Martin")
		self.assertEqual(profile.last_name, "Skow Roed")
		self.assertEqual(profile.email, 'test@test.no')

	def test_duplicate_profile_form(self):
		self.test_profile_creation_form()
		data = {'username': 'test', 'email': 'test@test.no', 'name': 'Martin Skow Roed', 'password1': 'martin'}
		form = ProfileCreationForm(data)
		self.assertFalse(form.is_valid())


	def test_socialprofile_creation_form(self):
		profile = Profile.objects.create(username='test', password='test')
		data = {'provider': 'twitter', 'token': '123', 'secret': '12313', 'handle': 'test'}
		form = SocialProfileCreationForm(profile, data)
		self.assertTrue(form.is_valid())
		socialProfile = form.save()
		self.assertEqual(socialProfile.token, '123')
		self.assertEqual(socialProfile.handle, 'test')
		self.assertEqual(socialProfile.provider, 'twitter')
		self.assertEqual(socialProfile.secret, '12313')
		form = SocialProfileCreationForm(profile, data)
		self.assertFalse(form.is_valid())
		del data['provider']
		form = SocialProfileCreationForm(profile, data)
		self.assertFalse(form.is_valid())
