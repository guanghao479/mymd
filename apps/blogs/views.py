from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from blogs.forms import PostForm
from blogs.models import Post
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
import datetime
from authority.decorators import permission_required_or_403, permission_required
from blogs.decorators import ownership_required

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
        return '/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BlogCreateView, self).dispatch(*args, **kwargs)


class BlogListView(ListView):
    """
    List all blogs of current user.
    """
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs_list'

    def get_queryset(self):
        username = self.kwargs.get('username')
        self.user = get_object_or_404(User, username=username)
        blogs = Post.objects.filter(author=self.user)
        return blogs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BlogListView, self).dispatch(*args, **kwargs)

class BlogDetailView(DetailView):
    template_name = 'blogs/blog_details.html'
    context_object_name = 'blog'

    def get_object(self):
        blog_class = Post
        post_id = self.kwargs.get('id')
        print post_id
        blog = get_object_or_404(blog_class, id=post_id)
        self.author = blog.author
        return blog

    def get_context_data(self, **kwargs):
        blog_author = self.author
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['blog_author'] = blog_author
        return context

def get_owner(request, *args, **kwargs):
    return Post.objects.get(pk=kwargs['id']).author

class BlogUpdateView(UpdateView):

    template_name = 'blogs/blog_edit.html'
    context_object_name = 'blog'
    form_class = PostForm
    def get_template_names(self):
        return [self.template_name]

    def get_success_url(self):
        return '/'

    def get_object(self, queryset=None):
        blog_class = Post
        post_id = self.kwargs.get('id')
        blog = Post.objects.get(pk=post_id)
        self.author = blog.author
        return blog

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.modified_date = datetime.datetime.now()
        blog.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(BlogUpdateView, self).get_context_data(**kwargs)
        context['blog_form'] = context['form']
        return context

    @method_decorator(ownership_required(get_owner))
    def dispatch(self, request, *args, **kwargs):
            return super(BlogUpdateView, self).dispatch(request, *args, **kwargs)


class BlogDeleteView(DeleteView):
    template_name = 'blogs/blog_delete.html'
    model = Post
    success_url = 'blog_list'
    context_object_name = 'blog'

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user})

    def get_object(self):
        blog_class = Post
        post_id = self.kwargs.get('id')
        print post_id
        blog = get_object_or_404(blog_class, id=post_id)
        self.author = blog.author
        return blog

    def get_context_data(self, **kwargs):
        context = super(BlogDeleteView, self).get_context_data(**kwargs)
        context['blog'] = kwargs.get('id')
        return context

