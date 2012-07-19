import authority
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()
from pinax.apps.account.openid_consumer import PinaxConsumer

handler500 = "pinax.views.server_error"

urlpatterns = patterns("",
    url(r"^$", "home.views.index", name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("profiles.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r"^avatar/", include("avatar.urls")),
    url(r"^friend/", include("friends.urls")),
    url(r"^activity/", include("actstream.urls")),
    url(r"^experience/$", direct_to_template, {'template': 'experience/index.html'}),
    url(r"^experience/new$", direct_to_template, {'template': 'experience/new.html'}),
    url(r"^pins/", include("pins.urls")),
    url(r"^blogs/", include("blogs.urls")),
    url(r"^diary/", include("diary.urls")),
    url(r"^comments/", include("django.contrib.comments.urls")),
    url(r"^search/", include("haystack.urls")),
    url(r"^stream/", include("stream.urls")),
    url(r"^(?P<username>[\w\._-]+)/$", "home.views.home", name="person_home"),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
    
if settings.DEBUG:
    urlpatterns += patterns("",
        (
        r'^site_media/media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}
        ),
    )
