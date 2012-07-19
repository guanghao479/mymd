from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from friends.models import *
from django.utils import simplejson as json
from friends.signals import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from actstream.models import user_stream, actor_stream

def stream_mine(request):
    result = {}
    #import pdb; pdb.set_trace()
    if not request.is_ajax():
        return render_to_response('stream/mine.html', RequestContext(request,{}))
    else:
        if not request.user.is_authenticated():
            result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
        else:
            result = { "success" : True, "stream" : stream_to_activities(actor_stream(request.user)) }
        return HttpResponse(json.dumps(result), content_type="application/json")

def stream_to_activities(stream):
    activities = []
    for action in stream:
        activity = {}
        activity['description'] = action.description
        activity['verb'] = action.verb
        activity['actor'] = unicode(action.actor)
        activity['target'] = unicode(action.target)
        activity['action_object'] = unicode(action.action_object)
        activity['timestamp'] = action.timestamp.strftime("%A %d %B %Y %I:%M%p")
        activity['string'] = unicode(activity)
        activities.append(activity)
    return activities
