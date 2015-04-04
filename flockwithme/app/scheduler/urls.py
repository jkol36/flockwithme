from django.conf.urls import patterns, include, url

viewpatterns = patterns('flockwithme.app.scheduler.views',
	url(r'^auto_dm/$', 'auto_dm', name='auto_dm'),
	url(r'^show_queue/$', 'show_queue', name='show_queue'),
	url(r'^delete_job/(?P<pk>\d+)/$', 'delete_job', name='delete_job'),
	url(r'^analytics/$', 'analytics_view', name='analytics'),
	url(r'^start/$', 'start', name='start'),
)

urlpatterns = viewpatterns