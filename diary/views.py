from django.utils.decorators import method_decorator
from django.utils import simplejson as json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from diary.models import Diary
from diary.forms import DiaryForm
from diary.utils import JSONResponseMixin

from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.http import Http404
import datetime
from mymdutils.decorators import ownership_required
from django.conf import settings

class DiaryCreateView(CreateView):
    """
    Create a new diary.
    """
    template_name = 'diary/diary_create.html'
    form_class = DiaryForm

    def get_template_names(self):
        return [self.template_name]

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.author = self.request.user
        diary.created_date = datetime.datetime.now()
        diary.modified_date = datetime.datetime.now()
        diary.publish_date = datetime.datetime.now()
        diary.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return '/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DiaryCreateView, self).dispatch(*args, **kwargs)

class DiaryListView(ListView):
    """
    List all diaries of current user.
    """
    template_name = 'diary/diary_list.html'
    context_object_name = 'diary_list'
    result = {}
    #paginate_by = settings.PAGINATE_NUM

    def get_queryset(self):
        self.user = self.request.user
        self.username = self.user.username
        diaries = Diary.objects.filter(author=self.user)
        return diaries

    def get_context_data(self, **kwargs):
        context = super(DiaryListView, self).get_context_data(**kwargs)
        context['username'] = self.username
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DiaryListView, self).dispatch(*args, **kwargs)

class DiaryDetailView(DetailView):
    template_name = 'diary/diary_details.html'
    context_object_name = 'diary'

    def get_object(self):
        diary_class = Diary
        diary_id = self.kwargs.get('id')
        diary = get_object_or_404(diary_class, id=diary_id)
        self.author = diary.author
        return diary

    def get_context_data(self, **kwargs):
        diary_author = self.author
        context = super(DiaryDetailView, self).get_context_data(**kwargs)
        context['diary_author'] = diary_author
        return context

def get_owner(request, *args, **kwargs):
    return Diary.objects.get(pk=kwargs['id']).author

class DiaryUpdateView(UpdateView):

    template_name = 'diary/diary_edit.html'
    context_object_name = 'diary'
    form_class = DiaryForm
    def get_template_names(self):
        return [self.template_name]

    def get_success_url(self):
        return '/'

    def get_object(self, queryset=None):
        experience_class = Diary
        diary_id = self.kwargs.get('id')
        diary = Diary.objects.get(pk=diary_id)
        self.author = diary.author
        return diary

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.author = self.request.user
        diary.modified_date = datetime.datetime.now()
        diary.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(DiaryUpdateView, self).get_context_data(**kwargs)
        context['diary_form'] = context['form']
        return context

    @method_decorator(ownership_required(get_owner))
    def dispatch(self, request, *args, **kwargs):
        return super(DiaryUpdateView, self).dispatch(request, *args, **kwargs)


class DiaryDeleteView(DeleteView):
    template_name = 'diary/diary_delete.html'
    model = Diary
    success_url = 'diary_list'
    context_object_name = 'diary'

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user})

    def get_object(self):
        diary_class = Diary
        diary_id = self.kwargs.get('id')
        diary = get_object_or_404(diary_class, id=diary_id)
        self.author = diary.author
        return diary

    def get_context_data(self, **kwargs):
        context = super(DiaryDeleteView, self).get_context_data(**kwargs)
        context['diary'] = kwargs.get('id')
        return context

    @method_decorator(ownership_required(get_owner))
    def dispatch(self, request, *args, **kwargs):
        return super(DiaryDeleteView, self).dispatch(request, *args, **kwargs)
