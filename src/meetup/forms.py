from django.contrib.auth.models import User
from django import forms
from meetup.models import Meetup
from redactor.widgets import RedactorEditor
from django.conf import settings

class MeetupForm(forms.ModelForm):
    content = forms.CharField(widget=RedactorEditor(
        redactor_settings=settings.REDACTOR_SETTINGS))
    class Meta:
        model = Meetup
        fields = ('title', 'content', 'date', 'city', 'address', 'poster')
