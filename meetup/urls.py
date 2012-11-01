from django.conf.urls.defaults import *

from meetup.views import MeetupCreateView, MeetupDetailView, MeetupListView, status, attend, attenders, mine

urlpatterns = patterns("meetup.views",
    url(r"^details/(?P<id>\d+)/$", MeetupDetailView.as_view(), name="meetup_detail"),
    url(r"^create/$", MeetupCreateView.as_view(), name="meetup_create"),
    url(r"^all/(?P<city>\d+)/$", MeetupListView.as_view(), name="meetup_list"),
    url(r"^attenders/$", attenders, name="meetup_attenders"),
    url(r"^attend/$", attend, name="meetup_attend"),
    url(r"^status/$", status, name="meetup_status"),
    url(r"^mine/$", mine, name="mine_meetup"),
)