from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView
from blogs.views import BlogCreateView
from blogs.models import Post

urlpatterns = patterns('blogs.views',
     url(r'^$', ListView.as_view(model=Post, template_name='blogs/blog_list.html'), name='blog_list'),
     url(r'^create/$', BlogCreateView.as_view(), name='blog_create'),
)

