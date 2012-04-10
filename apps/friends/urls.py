from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from friends.views import *

urlpatterns = patterns("",
    url(r"^$", my_friends, name="my_friends"),
    url(r"^add/$", add_as_friend, name="add_as_friend"),
    url(r"^status/$", status, name="add_as_friend"),
)