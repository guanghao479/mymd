from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from friends.models import FriendshipInvitation
from friends.signals import friends_connected

@receiver(friends_connected, sender=FriendshipInvitation)
def friend_action(sender, instance, **kwargs):
    action.send(instance.from_user, verb=u'connected', action_object=instance.to_user)
    action.send(instance.to_user, verb= u'connected', action_object=instance.from_user)