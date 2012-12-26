from django.contrib.auth.models import User
from django import forms
from diary.models import Diary
from tinymce.widgets import TinyMCE

class DiaryForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(
        mce_attrs={
            'theme' : "advanced",
            'theme_advanced_toolbar_location' : "top"
        }))

    class Meta:
        model = Diary
        fields = ('feel', 'body', 'status', 'privacy')
