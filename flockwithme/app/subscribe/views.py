from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .forms import SubscriberCreationForm
from django.contrib import messages


def subscribe(request):
	if request.POST:
		form = SubscriberCreationForm(request.POST)
		if form.is_valid():
			subscriber = form.save()
			messages.success(request, "You successfully subscribed")
		else:
			print form.errors
	return redirect(reverse('landingpage'))