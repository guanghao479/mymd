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

    class Meta:
        verbose_name = _("meetup")
        verbose_name_plural = _("meetups")

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('meetup_detail', [str(self.id)])

class Attend(models.Model):
    """
    User attend meetup relationship. We use attend relationship
    instead of directly use ManyToMany field because we may want
    to establish other relationships, like follow.
    """
    attender = models.ForeignKey(User)
    meetup = models.ForeignKey(Meetup)
    attend_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s-%s" % (self.attender, self.meetup)
