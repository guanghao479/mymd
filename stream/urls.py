from django.conf.urls.defaults import *
from stream.views import *

urlpatterns = patterns("",
    url(r"^$", stream, name="stream"),
    url(r"^mine/$", StreamMineView.as_view(), name="stream_mine"),
    url(r"^ajax/$", stream, name="stream_ajax"),
    url(r"^ajax/mine/$", stream_mine, name="stream_ajax_mine"),
)