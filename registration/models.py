import random
import datetime
import re
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.hashcompat import sha_constructor

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class RegistrationManager(models.Manager):
    def register(self, request, **kwargs):
        username, email, password = kwargs['username'], kwargs['email1'], kwargs['password']
        # Disable email sending for now
        new_user = self.create_inactive_user(username, email, password)
        return new_user

    def activate_user(self, request, activation_key):
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                activationObj = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not activationObj.activation_key_expired():
                user = activationObj.user
                user.is_active = True
                user.save()
                activationObj.activation_key = self.model.ACTIVATED
                activationObj.save()
                print user
                return user
        return False

    def create_inactive_user(self, username, email, password, send_email=False):
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()
        new_activation_key = self.create_activation_key(new_user)

        if send_email:
            new_activation_key.send_activation_email(new_user)

        return new_user

    def create_activation_key(self, user):
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = sha_constructor(salt + username).hexdigest()
        return self.create(user=user, activation_key=activation_key)


class RegistrationActivation(models.Model):
    ACTIVATED = u"ALREADY_ACTIVATED"

    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    objects = RegistrationManager()

    def __unicode__(self):
        return u'%s: %s' % (self.user.username, self.activation_key)

    def send_activation_email(self, user):
        self.user.email_user('Needs activation', self.activation_key, 'dingguanghao@gmail.com')

    def activation_key_expired(self):
        expiration_date = datetime.timedelta(days=15)
        return self.activation_key == self.ACTIVATED or (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True
