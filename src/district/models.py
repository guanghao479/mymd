from django.db import models
from django.utils.translation import ugettext_lazy as _
from city.models import City

class District(models.Model):
    """
    """
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City)

    class Meta:
        verbose_name = _('district')
        verbose_name_plural = _('districts')

    def __unicode__(self):
        return self.name
