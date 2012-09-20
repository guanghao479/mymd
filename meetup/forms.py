from django.contrib.auth.models import User
from django import forms
from meetup.models import Meetup


class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = ('title', 'content', 'date', 'city', 'address', 'poster')
