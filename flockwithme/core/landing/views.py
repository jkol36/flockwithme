from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.core.urlresolvers import reverse
from flockwithme.core.profiles.forms import ProfileCreationForm
from django.contrib import messages

def index(request):
	if request.user.is_authenticated():
		return redirect(reverse('dashboard'))
	if request.POST:
		form = ProfileCreationForm(request.POST)
		if form.is_valid():
			profile = form.save()
			user = auth.authenticate(username=profile.username, password=request.POST['password1'])
			if user:
				auth.login(request, user)
				return redirect(reverse('dashboard'))
		for x, z in form.errors.viewitems():
			messages.error(request, x + z.as_text())
		return render(request, 'landing.jade')

	return render(request, 'landing.jade')

def login(request):
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)
		if user:
			auth.login(request, user)
			return redirect(reverse('dashboard'))
	return render(request, 'landing.jade')
