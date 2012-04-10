from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from friends.models import *
from django.utils import simplejson as json

def add_as_friend(request):
    """
    Adding friends
    Currently taking AJAX request only

    """
    result = {}
    if not request.is_ajax():
        return Http404

    import logging
    logging.debug("Is this debug working?")

    if not request.user.is_authenticated():
        result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
    else:
        to_username = request.POST["to_user"]
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        if Friendship.objects.are_friends(to_user, from_user):
            result = { "error": { "code": "FRIENDSHIP_EXISTS", }, }
        elif FriendshipInvitation.objects.filter(from_user=to_user, to_user=from_user):
            result = { "error": { "code": "INVITATION_EXISTS", }, }
        else:
            new_inv = FriendshipInvitation(from_user=from_user, to_user=to_user)
            new_inv.save()
            if not new_inv:
                result = { "error": { "code": "INVITATION_CREATION_FAILED" } }
            else:
                result = { "success":True }

    return HttpResponse(json.dumps(result), content_type="application/json")

def my_friends(request):
    return HttpResponse()

def status(request):
    result = {}
    if not request.is_ajax():
        return Http404

    import logging
    logging.debug("Is this debug working?")

    if not request.user.is_authenticated():
        result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
    else:
        to_username = request.GET["to_user"]
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        if Friendship.objects.are_friends(to_user, from_user):
            result = { "friends": { "status": "FRIENDSHIP_EXISTS", }, }
        elif FriendshipInvitation.objects.filter(from_user=to_user, to_user=from_user):
            result = { "friends": { "status": "INVITATION_EXISTS", }, }
        elif FriendshipInvitation.objects.filter(from_user=from_user, to_user=to_user):
            result = { "friends": { "status": "INVITATION_MADE", }, }
        else:
            result = { "friends": { "status": "AVAILABLE"} }

    return HttpResponse(json.dumps(result), content_type="application/json")
