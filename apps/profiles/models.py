from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    User profile class. Inherit from ProfileBase of idios.
    """
    user = models.OneToOneField(User)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        )
    DISEASE_CHOICES = (
        (u'A', u'Alzheimer\'s'),
        (u'S', u'Stroke'),
        )
    city = models.CharField(_("city"), max_length=50)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True)
    disease = models.CharField(max_length=2, choices=DISEASE_CHOICES)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        kwargs={ "username": self.user.username }
        return reverse("profile_detail", kwargs=kwargs)