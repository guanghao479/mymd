from django.contrib.auth.models import User
from django import forms
from experiences.models import Post
from redactor.widgets import RedactorEditor
from django.conf import settings

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=RedactorEditor(
        redactor_settings=settings.REDACTOR_SETTINGS))

    class Meta:
        model = Post
        fields = ('title', 'body', 'status', 'allow_comments')
