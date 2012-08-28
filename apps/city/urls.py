from django.conf.urls.defaults import patterns, url, include
from community.views import *

urlpatterns = patterns('city.views',
    url(r"^single/$", "city_for_district", name='single_city_json'),
)