from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from city.models import City


class Meetup(models.Model):
    """
    Meetup app model.
    """
    organizer = models.ForeignKey(User, related_name='organizer')
    attenders = models.ManyToManyField(User, related_name='attenders')
    city  = models.ForeignKey(City)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()
    poster = models.ImageField(upload_to='images/poster/')

    class Meta:
        verbose_name = _("meetup")
        verbose_name_plural = _("meetups")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("meetup:meetup_detail", kwargs=kwargs)