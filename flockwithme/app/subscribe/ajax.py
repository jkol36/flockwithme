from django_ajax.decorators import ajax
from .forms import SubscriberCreationForm

@ajax
def subscribe(request):
	print 'fikk request'
	if request.POST:
		form = SubscriberCreationForm(request.POST)
		if form.is_valid():
			success = True
			subscriber = form.save()
		else:
			print form.errors
			success = False
	return {'success': success}