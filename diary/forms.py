from django.contrib.auth.models import User
from django import forms
from diary.models import Diary
from redactor.widgets import RedactorEditor
from django.conf import settings

class DiaryForm(forms.ModelForm):
    body = forms.CharField(widget=RedactorEditor(
        redactor_settings=settings.REDACTOR_SETTINGS))

    class Meta:
        model = Diary
        fields = ('feel', 'body', 'status', 'privacy')
