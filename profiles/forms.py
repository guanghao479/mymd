from django.contrib.auth.models import User
from django import forms
from profiles.models import Profile

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ["user"]