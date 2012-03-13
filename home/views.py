from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
    if request.user.is_authenticated():
        return render_to_response('home/home.html')
    else:
        form = AuthenticationForm(request)
        request.session.set_test_cookie()
        return render_to_response('home/index.html', locals())
