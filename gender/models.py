from django.db import models
from django.utils.translation import ugettext_lazy as _

class Gender(models.Model):
    """
    """
    type = models.CharField(max_length=20)

    class Meta:
        verbose_name = _('gender')
        verbose_name_plural = _('genders')

    def __unicode__(self):
        return self.type