from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from friends.models import *
from django.utils import simplejson as json
from friends.signals import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from actstream.models import user_stream, actor_stream
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class StreamListView(ListView):
    template_name = 'stream/stream_list.html'
    context_object_name = 'activity_list'
    paginate_by = settings.PAGINATE_NUM

    def get_queryset(self):
        return user_stream(self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StreamListView, self).dispatch(*args, **kwargs)

class StreamMineView(ListView):
    template_name = 'stream/stream_mine.html'
    context_object_name = 'activity_list'
    paginate_by = settings.PAGINATE_NUM

    def get_queryset(self):
        return actor_stream(self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StreamMineView, self).dispatch(*args, **kwargs)
