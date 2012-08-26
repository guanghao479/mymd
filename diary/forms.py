from django.contrib.auth.models import User
from django import forms
from diary.models import Diary

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('feel', 'body', 'status', 'privacy')
