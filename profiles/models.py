from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from disease.models import Disease
from city.models import City
from district.models import District
from community.models import Community
from gender.models import Gender

class Profile(models.Model):
    """
    User profile class. Inherit from ProfileBase of idios.
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User)
    community = models.ForeignKey(Community)
    disease = models.ForeignKey(Disease)
    gender = models.CharField(max_length=2,
                              choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        kwargs={ "username": self.user.username }
        return reverse("profile_detail", kwargs=kwargs)