import os
import uuid
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from city.models import City


from meetup import MEETUP_POSTER_STORAGE_DIR

def poster_file_path(instance=None, filename=None):
    storage_filename = "%s_%s" % (uuid.uuid4(), filename)
    return os.path.join(MEETUP_POSTER_STORAGE_DIR, storage_filename)

class Meetup(models.Model):
    """
    Meetup app model.
    """
    organizer = models.ForeignKey(User, related_name='organizer')
    attenders = models.ManyToManyField(User, related_name='attenders', through='Attend')
    city  = models.ForeignKey(City)
    address = models.CharField(max_length=300)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()
    created_date = models.DateField()
    modified_date = models.DateField()
    poster = models.ImageField(upload_to=poster_file_path)

    objects = models.Manager()

    class Meta:
        app_label = 'meetup'
        verbose_name = _("meetup")
        verbose_name_plural = _("meetups")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meetup:meetup_detail', args=[str(self.id)])

class AttendManager(models.Manager):
    """
    Attend manager for Attend relationship.
    """

    def is_attent(self, user, meetup):
        """
        Check whether the given user is already attent the given
        meetup.
        """
        if self.filter(attender=user, meetup=meetup).count() > 0:
            return True
        else:
            return False


class Attend(models.Model):
    """
    User attend meetup relationship. We use attend relationship
    instead of directly use ManyToMany field because we may want
    to establish other relationships, like follow.
    """
    attender = models.ForeignKey(User)
    meetup = models.ForeignKey(Meetup)
    attend_date = models.DateField(blank=True, null=True)

    objects = AttendManager()

    def __unicode__(self):
        return "%s-%s" % (self.attender, self.meetup)


#TODO: A invitation feature for meetup organizer to invite user
# has not attent the meetup yet.