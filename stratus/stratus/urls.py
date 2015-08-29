from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stratus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^gateway/$', 'stratus.views.gateway', name = 'login_reg'),
	url(r'^gateway/registration$', 'stratus.views.registration', name = 'registration'),
    url(r'^gateway/login', 'stratus.views.login', name = 'login'),
    url(r'^home/$', 'stratus.views.home', name = 'home'),
    url(r'^gateway/logout/$', 'stratus.views.logout', name = 'logout'),
    url(r'^register_drives$', 'stratus_drive.views.register_drives', name = 'register_drives'),
    url(r'^upload/$', 'stratus.views.upload', name = 'upload'),

)
