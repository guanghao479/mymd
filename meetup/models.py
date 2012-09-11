from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Meetup(models.Model):
    """
    Meetup app model.
    """
    organizer = models.ForeignKey(User)
    users = models.ManyToManyField(User)
    location  = models.CharField()
    title = models.CharField()
    content = models.TextField()
    date = models.DateField()
    poster = models.ImageField(upload_to='images/poster/')

    class Meta:
        verbose_name = _("meetup")
        verbose_name_plural = _("meetups")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("account:profile:profile_detail", kwargs=kwargs)