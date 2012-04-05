from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from idios.utils import get_profile_base

def index(request):
    if request.user.is_authenticated():
        base_profile_class = get_profile_base();
        profiles = base_profile_class.objects.filter(user=request.user)
        print profiles[0]
        if profiles[0].is_profile_filled:
            return render_to_response(reverse('index'), RequestContext(request,{}))
        else:
            return redirect(reverse('profile_detail', kwargs={'username':request.user}),  RequestContext(request,{}))
    else:
        return render_to_response('home/index.html', RequestContext(request, locals()))

