from django.test import TestCase
from flockwithme.core.profiles.models import Profile, SocialProfile
from .forms import JobCreationForm
from .models import Job, Hashtag, Location, TwitterUser, TwitterRelationship, TwitterStatus

class ScheduleTest(TestCase):
	def test_form(self):
		profile = Profile.objects.create(username='martin', password='martin')
		socialProfile = SocialProfile.objects.create(provider='twitter', handle='martolini', profile=profile)
		hashtag = Hashtag.objects.create(name='entrepreneur')
		location = Location.objects.create(name='philly')
		data = {'socialProfile': socialProfile.pk, 'profile': profile.pk,'radius': '20', 'action':Job.ACTION_CHOICES[0][0], 'hashtag': hashtag.pk, 'location': location.pk}
		form = JobCreationForm(data)
		if not form.is_valid():
			print form.errors
		self.assertTrue(form.is_valid())
		job = form.save()
		self.assertEqual(job.action, Job.ACTION_CHOICES[0][0])

	def test_relationship(self):
		profile = Profile.objects.create(username='martin', password='martin')
		socialProfile = SocialProfile.objects.create(provider='twitter', handle='martolini', profile=profile)
		twitterUser = TwitterUser.objects.create(twitter_id=123456, screen_name='martolini')
		twitterStatus = TwitterStatus.objects.create(twitter_id=123423)
		socialProfile.add_favorite(twitterStatus)
		self.assertEqual(socialProfile.get_favorites().count(), 1)
