from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from friends.models import *
from django.utils import simplejson as json
from friends.signals import *

def add_as_friend(request):
    """
    Adding friends
    Currently taking AJAX request only

    """
    result = {}
    if not request.is_ajax():
        return Http404

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
                friends_requested.send(sender=new_inv)

    return HttpResponse(json.dumps(result), content_type="application/json")

def accept(request):
    """
    accept friendship invitation
    Currently taking AJAX request only

    """
    result = {}
    if not request.is_ajax():
        return Http404

    if not request.user.is_authenticated():
        result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
    else:
        from_username = request.POST["to_user"]
        from_user = User.objects.get(username=from_username)
        to_user = request.user
        invite = FriendshipInvitation.objects.get(from_user=from_user, to_user=to_user);
        if not invite:
            result = { "error": { "code" : "NO_INVITATION_FOUND", }, }
        else:
            invite.accept()
            result = { "success":True }
            friends_connected.send(sender=invite)
    return HttpResponse(json.dumps(result), content_type="application/json")


def decline(request):
    """
    decline friendship invitation
    Currently taking AJAX request only

    """
    result = {}
    if not request.is_ajax():
        return Http404

    if not request.user.is_authenticated():
        result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
    else:
        from_username = request.POST["to_user"]
        from_user = User.objects.get(username=from_username)
        to_user = request.user
        invite = FriendshipInvitation.objects.get(from_user=from_user, to_user=to_user);
        if not invite:
            result = { "error": { "code" : "NO_INVITATION_FOUND", }, }
        else:
            invite.decline()
            result = { "success":True }
    return HttpResponse(json.dumps(result), content_type="application/json")


def ignore(request):
    """
    ignore friendship invitation
    Currently taking AJAX request only

    """
    result = {}
    if not request.is_ajax():
        return Http404

    if not request.user.is_authenticated():
        result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
    else:
        from_username = request.POST["to_user"]
        from_user = User.objects.get(username=from_username)
        to_user = request.user
        invite = FriendshipInvitation.objects.get(from_user=from_user, to_user=to_user);
        if not invite:
            result = { "error": { "code" : "NO_INVITATION_FOUND", }, }
        else:
            invite.ignore()
            result = { "success":True }
    return HttpResponse(json.dumps(result), content_type="application/json")

def my_friends(request):
    pass

def status(request):
    result = {}
    if not request.is_ajax():
        return Http404

    if not request.user.is_authenticated():
        result = { "error": { "code" : "NOT_AUTHENTICATED", }, }
    else:
        to_username = request.GET["to_user"]
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        if Friendship.objects.are_friends(to_user, from_user):
            result = { "friends": { "status": "FRIENDSHIP_EXISTS", }, }
        elif FriendshipInvitation.objects.filter(from_user=to_user, to_user=from_user).exclude(status__in=["3", "4", "5", "6", "7", "8"]):
            result = { "friends": { "status": "INVITATION_EXISTS", }, }
        elif FriendshipInvitation.objects.filter(from_user=from_user, to_user=to_user).exclude(status__in=["3", "4", "5", "6", "7", "8"]):
            result = { "friends": { "status": "INVITATION_MADE", }, }
        else:
            result = { "friends": { "status": "AVAILABLE"} }

    return HttpResponse(json.dumps(result), content_type="application/json")
