from django.db import models
from django.utils.translation import ugettext_lazy as _

class Disease(models.Model):
    """
    """
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    incidence = models.IntegerField()

    class Meta:
        verbose_name = _('disease')
        verbose_name_plural = _('diseases')

    def __unicode__(self):
        return self.name