from django.conf.urls import patterns, include, url

ajaxpatterns = patterns('flockwithme.app.notification.ajax',
	url(r'^seen/$', 'seen_view', name='seen'),

)

urlpatterns = ajaxpatterns