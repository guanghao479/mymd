from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView
from experiences.views import ExperienceCreateView, ExperienceListView, ExperienceDetailView, ExperienceUpdateView, ExperienceDeleteView
from experiences.models import Post

urlpatterns = patterns('experiences.views',
    url(r'^people/(?P<username>\w+)/$', ExperienceListView.as_view(), name='experience_list'),
    url(r'^create/$', ExperienceCreateView.as_view(), name='experience_create'),
    url(r'^edit/(?P<id>\d+)/$', ExperienceUpdateView.as_view(), name='experience_edit'),
    url(r'^delete/(?P<id>\d+)/$', ExperienceDeleteView.as_view(), name='experience_delete'),
    url(r'^(?P<id>\d+)/$', ExperienceDetailView.as_view(), name='experience_detail'),
)

