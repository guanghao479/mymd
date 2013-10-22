from django.db import models
from django.utils.translation import ugettext_lazy as _

class City(models.Model):
    """
    """
    country = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    size = models.IntegerField()

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def __unicode__(self):
        return self.name