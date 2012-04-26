from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from friends.views import *

urlpatterns = patterns("",
    url(r"^$", my_friends, name="my_friends"),
    url(r"^status/$", status, name="add_as_friend"),
    url(r"^add/$", add_as_friend, name="add_as_friend"),
    url(r"^accept/$", accept, name="accept_friendship_invite"),
    url(r"^decline/$", decline, name="decline_friendship_invite"),
    url(r"^ignore/$", ignore, name="ignore_friendship_invite"),
)