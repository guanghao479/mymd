import datetime
from django.db import models
from experiences.managers import ExperiencePublishManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from experiences.signals import experience_posted
from django.dispatch import receiver
from django.conf import settings
from taggit.managers import TaggableManager

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
    tags = TaggableManager()

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

    def print_details(self):
        return unicode(self.body)

    def print_details_ellipsis(self):
        return unicode(self.body)[:settings.STREAM_DETAILS_ELLIPSIS_LENGTH], len(unicode(self.body)) > settings.STREAM_DETAILS_ELLIPSIS_LENGTH


@receiver(models.signals.post_save, sender=Post)
def post_post_save_handler(sender, instance, created, **kwargs):
    if (created):
        experience_posted.send(sender=instance)