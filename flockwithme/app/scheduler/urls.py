from django.conf.urls import patterns, include, url

viewpatterns = patterns('flockwithme.app.scheduler.views',
	url(r'^auto_favorite/$', 'auto_favorite', name='auto_favorite'),
	url(r'^auto_follow/$', 'auto_follow', name='auto_follow'),
	url(r'^auto_unfollow/$', 'auto_unfollow', name='auto_unfollow'),
	url(r'^auto_dm/$', 'auto_dm', name='auto_dm'),
	url(r'^show_queue/$', 'show_queue', name='show_queue'),
	url(r'^delete_job/(?P<pk>\d+)/$', 'delete_job', name='delete_job'),
	url(r'^analytics/$', 'analytics_view', name='analytics'),
	url(r'^add_job/$', 'add_job', name='add_job'),
	url(r'api_status/$', 'api_status', name="api_status"),
)

urlpatterns = viewpatterns