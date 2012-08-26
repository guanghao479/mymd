from django.conf.urls.defaults import patterns, url, include
from community.views import *

urlpatterns = patterns('community.views',
    url(r"^$", "community_for_district", name='community_json'),
)