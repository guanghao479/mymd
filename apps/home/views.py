from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from idios.utils import get_profile_base
from django.contrib.auth.decorators import login_required
from friends.models import Friendship
from mymdutils.decorators import add_nav_search_form

@login_required
def home(request, **kwargs):
    """
    Home page for authenticated user. For current user, we display
    aggregated information page. For user who is current user's
    friend, we display friend home page. For user who is not current
    user's friend we display not friend home page.

    """
    current_user = request.user
    home_page_user = User.objects.get(username=kwargs.get('username'))
    if current_user.username == home_page_user.username:
        return render_to_response('home/home.html', RequestContext(request,{}))
    else:
        if Friendship.objects.are_friends(current_user, home_page_user):
            return render_to_response('home/home.html', RequestContext(request,{}))
        else:
            return render_to_response('home/stranger.html', RequestContext(request,{}))

def index(request):
    return render_to_response('home/index.html', RequestContext(request,{}))