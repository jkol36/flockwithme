from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'flockwithme.core.landing.views.index', name='landingpage'),
	url(r'^login/$', 'flockwithme.core.landing.views.login', name='login'),
	url(r'^subscribe/$', 'flockwithme.app.subscribe.ajax.subscribe', name='subscribe'),
    url(r'^dashboard/$', 'flockwithme.core.dashboard.views.index', name='dashboard'),
    # url(r'^notification/', include('flockwithme.app.notification.urls')),
    url(r'^profile/', include('flockwithme.core.profiles.urls')),
    url(r'^scheduler/', include('flockwithme.app.scheduler.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
