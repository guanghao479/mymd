from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated():
        return render_to_response('home/home.html', RequestContext(request,{}))
    else:
        form = AuthenticationForm(request)
        request.session.set_test_cookie()
        return render_to_response('home/index.html', RequestContext(request, locals()))

def profile(request, username):
    if request.user.is_authenticated():
        user = User.objects.filter(username=username)
        if (user):
            return render_to_response('home/profile.html', RequestContext(request,{}))
        else:
            return HttpResponse(status=404)
    else:
        form = AuthenticationForm(request)
        request.session.set_test_cookie()
        return render_to_response('home/index.html', RequestContext(request, locals()))
