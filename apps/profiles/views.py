from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.http import Http404
from mymdutils.decorators import ownership_required
from django.utils.decorators import method_decorator

from profiles.models import Profile
from profiles.forms import ProfileForm

class ProfileDetailView(DetailView):
    
    template_name = 'profiles/profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        
        username = self.kwargs.get('username')
        if username is None:
            username = self.request.user.username
        profile_class = Profile
        self.page_user = get_object_or_404(User, username=username)
        return get_object_or_404(profile_class, user=self.page_user)
    
    def get_context_data(self, **kwargs):

        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        is_me = self.request.user == self.page_user
        context.update({
            'is_me': is_me,
            'page_user': self.page_user,
        })
        return context

#def get_owner(request, *args, **kwargs):
#    return User.objects.get(useranme=kwargs['username'])

class ProfileUpdateView(UpdateView):
    
    template_name = "profiles/profile_edit.html"
    context_object_name = "profile"
    form_class = ProfileForm

    def get_template_names(self):
        return [self.template_name]
    
    def get_object(self):
        profile_class = Profile
        profile = profile_class.objects.get(user=self.request.user)
        return profile
    
    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context["profile_form"] = context["form"]
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

