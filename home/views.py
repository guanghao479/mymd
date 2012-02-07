from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    form = AuthenticationForm(request)
    request.session.set_test_cookie()
    c = {'form': form}
    return render_to_response('home/home.html', RequestContext(request, c))
