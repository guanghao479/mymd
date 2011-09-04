from django.contrib.auth.models import User, check_password
from django.core.validators import email_re

"""
Email Authentication Backend
Allows a user to sign in using an email/password pair
"""
class EmailAuthBackend:
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    """ Authenticate a user based on email address as the user name. """
    def authenticate(self, username=None, password=None):
        if  email_re.search(username):
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            # We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        else:
            return None

    """ Get a User object from the user_id. """
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
