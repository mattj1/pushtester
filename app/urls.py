from django.conf.urls import patterns, url

import views

# Create your views here.
urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^recents', views.get_recent),
	url(r'^add_apid', views.add_apid),
	url(r'^add_pushservice', views.add_pushservice),

	url(r'^send_devices', views.send_devices),

	url(r'^test', views.test),
	# url(r'^translate', views.translate, name='translate'),
 #    url(r'^$', views.index),
#    url(r'^login/(\w*)', views.login, name='login')
)
