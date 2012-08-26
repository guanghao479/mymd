from django.db import models
from diary.managers import DiaryManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from experiences.models import Post
import datetime

class Diary(models.Model):
    """
    Model for user diary.
    Each diary includes rate of motion, and an experience.
    """
    FEEL_CHOICES = (
        (1, _('Great')),
        (2, _('Good')),
        (3, _('Normal')),
        (4, _('Bad')),
        (5, _('Horrible')))
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Published')))
    PRIVACY_CHOICES = (
        (1, _('Public')),
        (2, _('Privacy')))
    feel = models.IntegerField(_('feel'), choices=FEEL_CHOICES)
    body = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    privacy = models.IntegerField(_('privacy'), choices=PRIVACY_CHOICES, default=2)
    publish_date = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created_date = models.DateTimeField(_('created'), auto_now_add=True)
    modified_date = models.DateTimeField(_('modified'), auto_now=True)

    objects = DiaryManager()

    class Meta:
        verbose_name = _('diary')
        verbose_name_plural = _('diaries')
        ordering = ('-created_date',)

    @models.permalink
    def get_absolute_url(self):
        return ('diary_details', [str(self.id)])
