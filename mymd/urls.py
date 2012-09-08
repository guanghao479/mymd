import authority
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

handler500 = "pinax.views.server_error"

urlpatterns = patterns("",
    url(r"^$", "home.views.index", name="home"),
    url(r"^admin/", include(admin.site.urls)),

    url(r"^user/$", "home.views.home", name="my_home"),
    url(r"^user/(?P<username>[\w\._-]+)/$", "home.views.home", name="user_home"),
    # User specific urls
    url(r"^account/", include("account.urls", namespace='account')),
    url(r"^friend/", include("friends.urls")),
    url(r"^notice/", include("notification.urls")),
    url(r"^activity/", include("actstream.urls")),
    url(r"^experience/", include("experiences.urls")),
    url(r"^diary/", include("diary.urls")),
    url(r"^stream/", include("stream.urls")),
    url(r"^avatar/", include("avatar.urls")),
    url(r"^comment/", include("django.contrib.comments.urls")),

    # Site specific urls
    url(r"^about/", include("about.urls")),
    url(r"^search/", include("haystack.urls")),
    url(r"^district/", include("district.urls")),
    url(r"^community/", include("community.urls")),

    # TODO: research to keep or to remove or to be replaced
    url(r"^pin/", include("pins.urls")),
)