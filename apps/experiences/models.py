from django.db import models
from experiences.managers import ExperiencePublishManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime

class Post(models.Model):
    """
    The experience post entry class.
    """
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Published')))
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish_date = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created_date = models.DateTimeField(_('created'), auto_now_add=True)
    modified_date = models.DateTimeField(_('modified'), auto_now=True)

    objects = ExperiencePublishManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        db_table = 'experience_posts'
        ordering = ('-publish_date',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('experience_detail', [str(self.id)])
