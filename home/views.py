from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect


def index(request):
    if request.user.is_authenticated():
        return render_to_response('home/home.html', RequestContext(request,{}))
    else:
        form = AuthenticationForm(request)
        c = {'form': form}
        request.session.set_test_cookie()
        return render_to_response('home/index.html', RequestContext(request, c))
