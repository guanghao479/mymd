from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from profiles.models import Profile
from district.models import District
from city.models import City

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ["user"]
        #This is for form fields reordering. Without this, fields are in 
        #an unexpected order.
        fields=['disease', 'birth_date', 'gender', 'city', 'district', 'community']

    city = forms.CharField(
        label = _("City")
    )
    district = forms.ChoiceField(
        choices = [(d.id, d.name) for d in District.objects.all()],
        label = _("District"),
    )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["city"] = forms.ModelChoiceField(queryset = City.objects.all(), empty_label=None)

