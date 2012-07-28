from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from staticapps.models import Address
from staticapps.models import Disease

class Profile(models.Model):
    """
    User profile class. Inherit from ProfileBase of idios.
    """
    user = models.OneToOneField(User)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        )

    address = models.ForeignKey(Address)
    disease = models.ForeignKey(Disease)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        kwargs={ "username": self.user.username }
        return reverse("profile_detail", kwargs=kwargs)