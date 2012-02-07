import datetime
from django.db import models
from django.contrib.auth.models import User

FRIENDSHIP_STATUS = (
    ("1", "Pending"),
    ("2", "Approved"),
    ("3", "Declined"),
    ("4", "Blocked"),
    ("5", "Deleted"),
)

class FriendshipManager(models.Manager):
    def are_friends(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).count() > 0:
            return True
        if self.filter(from_user=user2, to_user=user1).count() > 0:
            return True
        return False

    def friends_of_user(self, user):
        friends = []
        for friendship in self.filter(from_user=user).select_related(depth=1):
            friends.append({"friend": friendship.to_user, "friendship": friendship})
        for friendship in self.filter(to_user=user).select_related(depth=1):
            friends.append({"friend": friendship.from_user, "friendship": friendship})
        return friends

    def invite(self, user1, user2):
        if (not Friendship.objects.are_friends(user1, user2)):
            friendship = Friendship(to_user=self.to_user, from_user=self.from_user)
            friendship.status = "1"
            friendship.save()
            # TODO
            # Send out invitation

    def accept(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            friendship = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            friendship = self.filter(from_user=user2, to_user=user1)
        friendship.status = "2"

    def decline(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            friendship = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            friendship = self.filter(from_user=user2, to_user=user1)
        friendship.status = "3"

    def block(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            friendship = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            friendship = self.filter(from_user=user2, to_user=user1)
        friendship.status = "4"

    def remove(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            friendship = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            friendship = self.filter(from_user=user2, to_user=user1)
        friendship.status = "5"


class Friendship(models.Model):

    from_user = models.ForeignKey(User, verbose_name="user who requested")
    to_user = models.ForeignKey(User, verbose_name="user who is requested")
    status = models.CharField(max_length=1, choices=FRIENDSHIP_STATUS)
    requestTime = models.DateField(default=datetime.date.today)
    responseTime = models.DateField()
    objects = FriendshipManager()

    class Meta:
        unique_together = (('to_user', 'from_user'),)

        