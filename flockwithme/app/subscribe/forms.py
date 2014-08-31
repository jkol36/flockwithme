from django import forms
from .models import Subscriber

class SubscriberCreationForm(forms.ModelForm):
	class Meta:
		model = Subscriber
		fields = ['email',]