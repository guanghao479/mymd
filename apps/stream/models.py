from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from experiences.signals import experience_posted
from friends.models import FriendshipInvitation
from friends.signals import *
from actstream import action
from actstream.actions import follow

@receiver(friends_connected)
def friend_connected_action(sender, **kwargs):
    action.send(sender.from_user, verb=u'connected with', action_object=sender.to_user)
    action.send(sender.to_user, verb=u'connected with', action_object=sender.from_user)
    follow(sender.from_user, sender.to_user)
    follow(sender.to_user, sender.from_user)

@receiver(experience_posted)
def experience_posted_action(sender, **kwargs):
    action.send(sender.author, verb=u'posted', action_object=sender)