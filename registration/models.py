from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class RegistrationManager(models.Manager):

    def activate_user():
        return False

    def create_inactive_user(self, username, email, password, send_email=True):
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        new_activation_key = RegistrationActivation.create_activation_key(new_user)

        if send_email:
            self.send_activation_email()

        return new_user

    def send_activation_email(self, user, activation_key):
        return False


class Activation(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    test = models.CharField(_('test'), max_length=5)

    objects = RegistrationManager()

    def create_activation_key(self, user):
        return None

