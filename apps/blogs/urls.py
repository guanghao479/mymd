from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView
from blogs.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView
from blogs.models import Post

urlpatterns = patterns('blogs.views',
     url(r'^people/(?P<username>\w+)/$', BlogListView.as_view(), name='blog_list'),
     url(r'^create/$', BlogCreateView.as_view(), name='blog_create'),
     url(r'^(?P<id>\d+)/$', BlogDetailView.as_view(), name='blog_detail'),
     url(r'^edit/(?P<id>\d+)/$', BlogUpdateView.as_view(), name='blog_edit'),
     url(r'^delete/(?P<id>\d+)/$', BlogDeleteView.as_view(), name='blog_delete'),
)

