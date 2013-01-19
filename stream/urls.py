from django.conf.urls.defaults import *
from stream.views import *

urlpatterns = patterns("",
    url(r"^$", StreamListView.as_view(), name="stream_list"),
    url(r"^mine/$", StreamMineView.as_view(), name="stream_mine"),
)