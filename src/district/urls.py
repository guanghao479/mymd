from django.conf.urls.defaults import patterns, url, include
from district.views import *

urlpatterns = patterns('district.views',
    url(r"^$", "district_for_city", name='district_json'),
)