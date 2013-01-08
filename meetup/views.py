import datetime
import uuid
import os
from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView, ListView
from city.models import City
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from meetup.forms import MeetupForm
from meetup.models import Meetup, Attend
from django.utils import simplejson as json
from django.db.models import Q
from itertools import chain

def get_poster_path(instance=None, filename=None):
    storage_filename = "%s_%s" % (uuid.uuid4(), filename)
    return os.path.join(
        settings.MEETUP_POSTER_STORAGE_DIR,
        storage_filename)


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
        poster_path = get_poster_path(filename=self.request.FILES['poster'].name)
        poster_storage_path = os.path.join(settings.MEDIA_ROOT, poster_path)

        meetup.poster=poster_path
        meetup.poster.storage.save(poster_storage_path, self.request.FILES['poster'])
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
        context['meetup'] = self.meetup
        return context

def attend(request):
    """
    View for user to attend meetup.
    """
    result = {}
    if not request.is_ajax():
        return Http404
    if not request.user.is_authenticated():
        result = { 'error': { 'code' : 'NOT_AUTHENTICATED', }, }
    else:
        meetup_id = request.POST['meetup']
        meetup = Meetup.objects.get(id=meetup_id)
        attender = request.user
        if Attend.objects.is_attendee(meetup=meetup, user=attender):
            result = { 'error': { 'code': 'ALREADY_ATTENT', }, }
        else:
            new_attender = Attend(attender=attender,
                                  meetup=meetup,
                                  attend_date=datetime.datetime.now())
            new_attender.save()
            if not new_attender:
                result = { 'error': { 'code': 'ATTEND_RELATIONSHIP_CREATION_FAILED' } }
            else:
                result = { 'success':True }

    return HttpResponse(json.dumps(result), content_type='application/json')

def attenders(request):
    """
    View for list all attenders for a given meetup.
    """
    result = {}
    if not request.is_ajax():
        return Http404
    if not request.user.is_authenticated():
        result = { 'error': { 'code' : 'NOT_AUTHENTICATED', }, }
    else:
        attenders = []
        meetup_id = request.GET['meetup']
        meetup = Meetup.objects.get(id=meetup_id)
        attend_relationships = Attend.objects.filter(meetup=meetup)
        for attend_relationship in attend_relationships:
            attender = {'name': attend_relationship.attender.username}
            attenders.append(attender)
        result = {'attenders': attenders}
    return HttpResponse(json.dumps(result), content_type='application/json')

def status(request):
    """
    View to check user whether already attent the given meetup.
    """
    result = {}
    if not request.is_ajax():
        return Http404
    if not request.user.is_authenticated():
        result = {'error': { 'code' : 'NOT_AUTHENTICATED', }, }
    else:
        user = request.user
        meetup = request.GET['meetup']
        if Attend.objects.is_attendee(meetup=meetup, user=user):
            result = {'meetup': { 'status': 'ATTENT', }, }
        else:
            result = {'meetup': { 'status': 'AVAILABLE'}, }
    return HttpResponse(json.dumps(result), content_type="application/json")

def mine(request, template='meetup/meetup_mine.html'):
    """
    Current user meetups information.

    """
    context = {'request': request}
    user = request.user

    meetups_organized = Meetup.objects.filter(organizer=user)
    meetups_attended = user.meetups_attended.all()
    context['meetups'] = meetups_organized | meetups_attended
    response = render_to_response(template, RequestContext(request, context))

    return response