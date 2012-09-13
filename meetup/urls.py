from django.conf.urls.defaults import *

from meetup.views import MeetupDetailView, MeetupListView

urlpatterns = patterns("meetup.views",
    url(r"^(?P<city>[\w\._-]+)/$", MeetupListView.as_view(), name="meetup_list"),
    url(r"^details/(?P<id>\d+)/$", MeetupDetailView.as_view(), name="meetup_details"),
)