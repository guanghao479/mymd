from django.db import models
from django.utils.translation import ugettext_lazy as _


from idios.models import ProfileBase


class Profile(ProfileBase):
    """
    User profile class. Inherit from ProfileBase of idios.
    """
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
