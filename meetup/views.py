from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from city.models import City
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings

class MeetupListView(ListView):
    """
    List all meetups of a given city.
    """
    template_name = 'meetup/meetup_list.html'
    context_object_name = 'meetup_list'
    paginate_by = settings.PAGINATE_NUM

    def get_queryset(self):
        self.cityname = self.kwargs.get('city')
        self.city = get_object_or_404(City, name=self.city)
        meetups = Meetup.objects.filter(city=self.city)
        return meetups

    def get_context_data(self, **kwargs):
        context = super(MeetupListView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MeetupListView, self).dispatch(*args, **kwargs)

class MeetupDetailView(DetailView):
    
    template_name = 'meetup/meetup.html'
    context_object_name = 'meetup'
    
    def get_object(self):
        meetup_id = self.kwargs.get('id')
        meetup_class = Meetup
        self.meetup = get_object_or_404(meetup_class, pk=meetup_id)
        return self.meetup
    
    def get_context_data(self, **kwargs):
        context = super(MeetupDetailView, self).get_context_data(**kwargs)
        return context
