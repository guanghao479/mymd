from django.conf.urls.defaults import *

from meetup.views import MeetupCreateView, MeetupDetailView, MeetupListView

urlpatterns = patterns("meetup.views",
    url(r"^details/(?P<id>\d+)/$", MeetupDetailView.as_view(), name="meetup_detail"),
    url(r"^create/$", MeetupCreateView.as_view(), name="meetup_create"),
    url(r"^all/(?P<city>\d+)/$", MeetupListView.as_view(), name="meetup_list"),
)