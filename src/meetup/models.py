from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from city.models import City
from django.conf import settings
from taggit.managers import TaggableManager

class Meetup(models.Model):
    """
    Meetup app model.
    """
    organizer = models.ForeignKey(User, related_name='meetups_organi')
    attenders = models.ManyToManyField(User, related_name='meetups_attended', through='Attend')
    city  = models.ForeignKey(City)
    address = models.CharField(max_length=300)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()
    created_date = models.DateField()
    modified_date = models.DateField()
    poster = models.ImageField(upload_to="static/images/meetups")

    objects = models.Manager()
    tags = TaggableManager()

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

    def is_attendee(self, user, meetup):
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