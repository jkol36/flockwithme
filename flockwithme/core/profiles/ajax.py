from django_ajax.decorators import ajax
from django.contrib.auth.decorators import login_required
from .models import Profile, SocialProfile
from .forms import SocialProfileCreationForm

@ajax
@login_required
def associate_provider(request):
	if request.POST:
		form = SocialProfileCreationForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			success = True
		else:
			print form.errors
			success = False
		return {'success': success}

