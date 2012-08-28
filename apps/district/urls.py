from django.conf.urls.defaults import patterns, url, include
from district.views import *

urlpatterns = patterns('district.views',
    url(r"^$", "district_for_city", name='district_json'),
    url(r"^single/$", "district_for_community", name='single_district_json'),
)