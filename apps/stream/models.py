from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from friends.models import FriendshipInvitation
from friends.signals import *
from actstream import action, follow

@receiver(friends_connected)
def friend_connected_action(sender, **kwargs):
    action.send(sender.from_user, verb=u'connected', action_object=sender.to_user)
    action.send(sender.to_user, verb=u'connected', action_object=sender.from_user)
    follow(sender.from_user, sender.to_user)
    follow(sender.to_user, sender.from_user)

@receiver(friends_requested)
def friend_requested_action(sender, **kwargs):
    action.send(sender.from_user, verb=u'requested', action_object=sender.to_user)