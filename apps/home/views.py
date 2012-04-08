from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from idios.utils import get_profile_base

def index(request):
    """
    View for index page. When user is authenticated, we check whether
    or not this user is complete his profile, here we just using city
    to check profile completion, because only when a user is first sign
    up, the city can be leave as blank. So I think it's OK for now.

    """
    if request.user.is_authenticated():
        base_profile_class = get_profile_base();
        profiles = base_profile_class.objects.filter(user=request.user)
        if profiles[0].city != "":
            print profiles[0].city
            return render_to_response('home/home.html', RequestContext(request,{}))
        else:
            return redirect(reverse('profile_edit'), RequestContext(request,{}))
    else:
        return render_to_response('home/index.html', RequestContext(request, {}))

