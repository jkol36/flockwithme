from django.config.urls import patterns, include, url 


urlpatterns = ('',
	url(r'^help/$', 'dashboard.views.help' name = 'help'),
	)
