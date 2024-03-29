from django.conf.urls.defaults import *

from profiles.views import ProfileDetailView, ProfileUpdateView


urlpatterns = patterns("profiles.views",
    url(r"^edit/$", ProfileUpdateView.as_view(), name="profile_edit"),
    url(r"^details/(?P<username>[\w.@+-]+)/$", ProfileDetailView.as_view(), name="profile_detail"),
)