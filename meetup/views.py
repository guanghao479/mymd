import datetime
import pdb

from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView, ListView
from city.models import City
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render_to_response

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from meetup.forms import MeetupForm
from meetup.models import Meetup, poster_file_path

class MeetupCreateView(CreateView):
    """
    Create a new meetup.
    """
    template_name = 'meetup/meetup_create.html'
    form_class = MeetupForm

    def get_template_names(self):
        return [self.template_name]

    def form_valid(self, form):
        meetup = form.save(commit=False)
        #pdb.set_trace()
        poster_path = poster_file_path(filename=self.request.FILES['poster'].name)
        meetup.poster=poster_path
        meetup.poster.storage.save(poster_path, self.request.FILES['poster'])
        meetup.organizer = self.request.user
        meetup.created_date = datetime.datetime.now()
        meetup.modified_date = datetime.datetime.now()
        meetup.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return '/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MeetupCreateView, self).dispatch(*args, **kwargs)

class MeetupListView(ListView):
    """
    List all meetups of a given city.
    """
    template_name = 'meetup/meetup_list.html'
    context_object_name = 'meetup_list'
    paginate_by = settings.PAGINATE_NUM

    def get_queryset(self):
        self.cityid = self.kwargs.get('city')
        self.city = get_object_or_404(City, id=self.cityid)
        meetups = Meetup.objects.filter(city=self.city)
        return meetups

    def get_context_data(self, **kwargs):
        context = super(MeetupListView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MeetupListView, self).dispatch(*args, **kwargs)

class MeetupDetailView(DetailView):
    
    template_name = 'meetup/meetup_datail.html'
    context_object_name = 'meetup'
    
    def get_object(self):
        meetup_id = self.kwargs.get('id')
        meetup_class = Meetup
        self.meetup = get_object_or_404(meetup_class, pk=meetup_id)
        return self.meetup
    
    def get_context_data(self, **kwargs):
        context = super(MeetupDetailView, self).get_context_data(**kwargs)
        return context
