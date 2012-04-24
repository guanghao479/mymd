from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blogs.forms import PostForm
from blogs.models import Post
from django.shortcuts import redirect, get_object_or_404
import datetime

class BlogCreateView(CreateView):
    """
    Create a new blog.
    """
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
    def dispatch(self, *args, **kwargs):
        return super(BlogCreateView, self).dispatch(*args, **kwargs)


class BlogListView(ListView):
    """
    List all blogs of current user.
    """
    template_name = "blogs/blogs.html"
    context_object_name = "blogs_list"

    def get_queryset(self):
        username = self.kwargs.get('username')
        self.user = get_object_or_404(User, username=username)
        blogs = Post.objects.filter(author=self.user)
        return blogs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BlogListView, self).dispatch(*args, **kwargs)

class BlogDetailView(DetailView):
    template_name = "blogs/blog_details.html"
    context_object_name = "blog"

    def get_object(self):
        blog_class = "Post"
        post_id = self.kwargs.get('id')
        return get_object_or_404(blog_class, pk=post_id)
