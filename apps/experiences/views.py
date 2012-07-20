from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from experiences.forms import PostForm
from experiences.models import Post
from friends.models import Friendship, FriendshipManager
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
import datetime
from authority.decorators import permission_required_or_403, permission_required
from mymdutils.decorators import ownership_required
from django.conf import settings

class ExperienceCreateView(CreateView):
    """
    Create a new experience.
    """
    template_name = 'experiences/experience_create.html'
    form_class = PostForm

    def get_template_names(self):
        return [self.template_name]

    def form_valid(self, form):
        experience = form.save(commit=False)
        experience.author = self.request.user
        experience.created_date = datetime.datetime.now()
        experience.modified_date = datetime.datetime.now()
        experience.publish_date = datetime.datetime.now()
        experience.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return '/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExperienceCreateView, self).dispatch(*args, **kwargs)


class ExperienceListView(ListView):
    """
    List all experiences of current user.
    """
    template_name = 'experiences/experience_list.html'
    context_object_name = 'experiences_list'
    paginate_by = settings.PAGINATE_NUM

    def get_queryset(self):
        self.username = self.kwargs.get('username')
        self.user = get_object_or_404(User, username=self.username)
        experiences = Post.objects.filter(author=self.user)
        return experiences

    def get_context_data(self, **kwargs):
        context = super(ExperienceListView, self).get_context_data(**kwargs)
        friends_object_list = Friendship.objects.friends_for_user(self.user)
        friends = []
        for friend in friends_object_list:
            friends.append(friend.get('friend'))
        context['friends'] = friends
        context['username'] = self.username
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExperienceListView, self).dispatch(*args, **kwargs)

class ExperienceDetailView(DetailView):
    template_name = 'experiences/experience_details.html'
    context_object_name = 'experience'

    def get_object(self):
        experience_class = Post
        post_id = self.kwargs.get('id')
        experience = get_object_or_404(experience_class, id=post_id)
        self.author = experience.author
        return experience

    def get_context_data(self, **kwargs):
        experience_author = self.author
        context = super(ExperienceDetailView, self).get_context_data(**kwargs)
        context['experience_author'] = experience_author
        return context

def get_owner(request, *args, **kwargs):
    return Post.objects.get(pk=kwargs['id']).author

class ExperienceUpdateView(UpdateView):

    template_name = 'experiences/experience_edit.html'
    context_object_name = 'experience'
    form_class = PostForm
    def get_template_names(self):
        return [self.template_name]

    def get_success_url(self):
        return '/'

    def get_object(self, queryset=None):
        experience_class = Post
        post_id = self.kwargs.get('id')
        experience = Post.objects.get(pk=post_id)
        self.author = experience.author
        return experience

    def form_valid(self, form):
        experience = form.save(commit=False)
        experience.author = self.request.user
        experience.modified_date = datetime.datetime.now()
        experience.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ExperienceUpdateView, self).get_context_data(**kwargs)
        context['experience_form'] = context['form']
        return context

    @method_decorator(ownership_required(get_owner))
    def dispatch(self, request, *args, **kwargs):
        return super(ExperienceUpdateView, self).dispatch(request, *args, **kwargs)


class ExperienceDeleteView(DeleteView):
    template_name = 'experiences/experience_delete.html'
    model = Post
    success_url = 'experience_list'
    context_object_name = 'experience'

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user})

    def get_object(self):
        experience_class = Post
        post_id = self.kwargs.get('id')
        print post_id
        experience = get_object_or_404(experience_class, id=post_id)
        self.author = experience.author
        return experience

    def get_context_data(self, **kwargs):
        context = super(ExperienceDeleteView, self).get_context_data(**kwargs)
        return context

    @method_decorator(ownership_required(get_owner))
    def dispatch(self, request, *args, **kwargs):
        return super(ExperienceDeleteView, self).dispatch(request, *args, **kwargs)
