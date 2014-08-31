from django.conf.urls import patterns, include, url

ajax_patterns = patterns('flockwithme.core.profiles.ajax',
	url(r'^ajax/add_account/$', 'associate_provider', name='associate_provider'),
)

viewpatterns = patterns('flockwithme.core.profiles.views',
	url(r'^accounts/$', 'my_accounts', name='my_accounts'),
	url(r'^hashtags/$', 'my_hashtags', name='my_hashtags'),
	url(r'^locations/$', 'my_locations', name='my_locations'),
	url(r'^influencers/$','my_influencers', name = 'my_influencers'),
	#url(r'^lists/$', 'my_lists', name = 'my_lists'),
	url(r'^logout/$', 'logout_view', name='logout'),
)

urlpatterns = ajax_patterns + viewpatterns