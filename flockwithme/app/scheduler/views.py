from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .forms import StartForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job
from flockwithme.core.profiles.models import SocialProfile
from django.utils import timezone
from datetime import timedelta

@login_required
def analytics_view(request):
	if request.GET:
		socialprofile = request.user.accounts.get(pk=request.GET.get('sp_pk'))
		data = {}
		since = (timezone.localtime(timezone.now()) - timedelta(days=7)).replace(minute=0, hour=0, second=0)
		until = since.replace(minute=59, hour=23, second=59)
		for _ in range(8):
			data[until.strftime("%Y-%m-%d")] = socialprofile.relationships.filter(action="FOLLOWER", created_at__range=[since, until]).count()
			until += timedelta(days=1)
	else:
		try:
			accounts = request.user.accounts.all()
			account = accounts[0]
			data = {}
			return render(request, 'analytics.jade', {'data': data})

		except Exception, AccountDoesNotExist:
			messages.error(request, "please add an account first")
			return redirect("my_accounts")

def handle_form(request):
	form = StartForm (request.user)
	form.save()
	messages.success(request, "Smile! :) Your social media marketing is now being handles by us. Focus your energy elsewhere!")

@login_required
def start(request):
	if not request.POST:
		return render(request, 'start.jade')
	handle_form(request)
	return render(request, 'start.jade')
		
		
@login_required
def auto_dm(request):
	if request.POST:
		try:
			handle_form(request)
			return render(request, 'auto_dm.jade')
		except Exception, e:
			messages.error(request, "Something went wrong. If the problem persists please email us.")


	try:
		accounts = request.user.accounts.all()
		pk = accounts[0].id
		return render(request, "auto_dm.jade")
	except Exception, NoAccounts:
		messages.error(request, "Please add a Twitter Account First.")
		return redirect("my_accounts")

	
			




@login_required
def delete_job(request, pk=None):
	if pk:
		try:
			job = Job.objects.get(pk=pk)
			if job.socialprofile.profile == request.user:
				messages.success(request, "Job successfully deleted!")
				job.delete()
		except:
			messages.error(request, "There is no such job, or you do not own that job.")
	return redirect(reverse('show_queue'))

@login_required
def show_queue(request):
	return render(request, 'show_queue.jade', {'jobs': Job.objects.filter(socialprofile__profile=request.user).exclude(action="TRACK_FOLLOWERS")})