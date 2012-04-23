from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blogs.forms import PostForm
from django.shortcuts import redirect
import datetime

class BlogCreateView(CreateView):
    template_name = 'blogs/blog_create.html'
    form_class = PostForm

    def get_template_names(self):
        return [self.template_name]

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.created_date = datetime.datetime.now()
        blog.modified_date = datetime.datetime.now()
        blog.publish_date = datetime.datetime.now()
        blog.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return "/blogs"

    @method_decorator(login_required)
    def dispath(self, *args, **kwargs):
        return super(BlogCreateView, self).dispatch(*args, **kwargs)
