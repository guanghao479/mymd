from django.conf.urls.defaults import *
from stream.views import *

urlpatterns = patterns("",
    url(r"^mine/$", stream_mine, name="stream_mine"),
)