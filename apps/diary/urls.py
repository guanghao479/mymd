from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView
from diary.views import *
from diary.models import Diary

urlpatterns = patterns('diary.views',
    url(r"^mine/$", DiaryListView.as_view(), name='diary_json'),
    url(r"^user/(?P<username>\w+)/$", DiaryListView.as_view(), name='diary_list'),
    url(r"^create/$", DiaryCreateView.as_view(), name='diary_create'),
    url(r"^detail/(?P<id>\d+)/$", DiaryDetailView.as_view(), name='diary_detail'),
    url(r"^edit/(?P<id>\d+)/$", DiaryUpdateView.as_view(), name='diary_edit'),
    url(r"^delete/(?P<id>\d+)/$", DiaryDeleteView.as_view(), name='diary_delete'),
)
