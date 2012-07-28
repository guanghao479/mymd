from django.db import models
from django.utils.translation import ugettext_lazy as _

class Address(models.Model):
	"""
	"""
	country = models.CharField(max_length=10)
	city = models.CharField(max_length=50)
	district = models.CharField(max_length=30)
	community = models.CharField(max_length=100)
	x_coodinate = models.IntegerField()
	y_coodinate = models.IntegerField()

	class Meta:
            verbose_name = _('address')
            verbose_name_plural = _('addresss')

        def __unicode__(self):
            return self.city+self.district+self.community


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

