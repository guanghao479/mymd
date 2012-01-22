from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.home'),
)

if settings.DEBUG:
    #### Admin
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    )

urlpatterns += patterns('',
    # url(r'^mymd/', include('mymd.foo.urls')),
    # url(r'^login/$', 'django.contrib.auth.views.login', {
    #    'template_name': 'auth/login.html'}),
    url(r'^/$', 'home.views.home', name='index'),
    url(r'^register/$', 'registration.views.register', name='register'),
    url(r'^register/needs_activation/$', 'registration.views.needs_activation', name='needs_activation'),
    url(r'^login/$', 'registration.views.login', name='login'), # Using default registration/login.html
    url(r'^activate/(?P<activation_key>\w+)/$', 'registration.views.activate'),
    url(r'^activate/$', 'registration.views.activate'),
    url(r'^user/(?P<username>\w+)/$', 'home.views.home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/profile/$', 'home.views.home'),
)
