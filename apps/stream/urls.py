from django.conf.urls.defaults import *
from stream.views import *

urlpatterns = patterns("",
    url(r"^$", stream, name="stream"),
    url(r"^mine/$", stream_mine, name="stream_mine"),
)