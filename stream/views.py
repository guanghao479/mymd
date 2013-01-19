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

def stream(request):
    result = {}
    if not request.is_ajax():
        return render_to_response('stream/index.html', RequestContext(request,{}))
    else:
        if not request.user.is_authenticated():
            result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
        else:
            result = { "success" : True, "stream" : stream_to_activities(user_stream(request.user)) }
        return HttpResponse(json.dumps(result), content_type="application/json")

def stream_mine(request):
    result = {}
    if not request.is_ajax():
        return render_to_response('stream/mine.html', RequestContext(request,{}))
    else:
        if not request.user.is_authenticated():
            result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
        else:
            result = { "success" : True, "stream" : stream_to_activities(actor_stream(request.user)) }
        return HttpResponse(json.dumps(result), content_type="application/json")

class StreamMineView(ListView):
    template_name = 'stream/stream_mine.html'
    context_object_name = 'activity_list'
    paginate_by = settings.PAGINATE_NUM

    def get_queryset(self):
        return actor_stream(self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StreamMineView, self).dispatch(*args, **kwargs)


def stream_to_activities(stream):
    #import pdb;pdb.set_trace();
    activities = []
    for action in stream:
        activity = {}
        activity['description'] = action.description
        activity['actor'] = {
            "name":unicode(action.actor),
            "url":action.actor.get_absolute_url()
            }
        activity['verb'] = action.verb
        if action.action_object:
            activity['action_object'] = {
                "name":unicode(action.action_object),
                "url":action.action_object.get_absolute_url()
                }
        if action.target:
            activity['target'] = {
                "name":unicode(action.target),
                "url":action.target.get_absolute_url()
                }
        activity['timestamp'] = action.timestamp.strftime("%A %d %B %Y %I:%M%p")
        activity['string'] = unicode(activity)
        if hasattr(action.action_object, 'print_details'):
            activity['details'] = action.action_object.print_details()
        activities.append(activity)
    return activities
