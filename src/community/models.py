from django.db import models
from django.utils.translation import ugettext_lazy as _
from district.models import District

class Community(models.Model):
    """
    """
    district = models.ForeignKey(District)
    name = models.CharField(max_length=100)
    x_coodinate = models.IntegerField()
    y_coodinate = models.IntegerField()

    class Meta:
        verbose_name = _('community')
        verbose_name_plural = _('communities')

    def __unicode__(self):
        return self.name