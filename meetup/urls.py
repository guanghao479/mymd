from django.conf.urls.defaults import *

from meetup.views import MeetupCreateView, MeetupDetailView, MeetupListView, status

urlpatterns = patterns("meetup.views",
    url(r"^details/(?P<id>\d+)/$", MeetupDetailView.as_view(), name="meetup_detail"),
    url(r"^create/$", MeetupCreateView.as_view(), name="meetup_create"),
    url(r"^all/(?P<city>\d+)/$", MeetupListView.as_view(), name="meetup_list"),
    url(r"^status/$", status, name="meetup_status"),
)