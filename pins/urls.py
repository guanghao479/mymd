from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from pins.views import *

urlpatterns = patterns("",
    url(r"^$", home, name="pins_home"),
)