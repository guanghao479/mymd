from django.contrib.auth.models import User
from registration.models import RegistrationActivation
from django.test import TestCase
from django.core import mail
from django.conf import settings
import datetime
import re

class RegistrationModelTestCases(TestCase):
    """
    Test the registration model including RegistrationManager
    RegistrationProfile and RegistrationActivation.

    """

    user_infor = {'username': 'example',
                  'email': 'example@example.com',
                  'password': '123456'}
    def setUp(self):
        self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
        settings.ACCOUNT_ACTIVATION_DAYS = 7

    def tearDown(self):
        settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation

    def test_inactive_user_creation(self):
        """
        Create a new user, set user data correctly, and
        sets the user's account as inactive.

        """
        new_user = RegistrationActivation.objects.create_inactive_user(**self.user_infor)
        self.assertEqual(new_user.username, 'example')
        self.assertEqual(new_user.email, 'example@example.com')
        self.failUnless(new_user.check_password('123456'))
        self.failIf(new_user.is_active)
        saved_user = User.objects.get(email__iexact='example@example.com')
        self.assertIsNotNone(saved_user)

    def test_profile_creation(self):
        """
        Create a registration Activation for a user. We should check
        the activation with correct user data and a SHA1 hash to use
        as activation key.

        """
        new_user = User.objects.create_user(**self.user_infor)
        activation = RegistrationActivation.objects.create_activation_key(new_user)

        self.assertEqual(RegistrationActivation.objects.count(), 1)
        self.assertEqual(activation.user.id, new_user.id)
        self.failUnless(re.match('^[a-f0-9]{40}$', activation.activation_key))

    def test_user_creation_email(self):
        """
        By default, create an inactive user, site should send an email.

        """
        new_user = RegistrationActivation.objects.create_inactive_user(send_email=True,
                                                                       **self.user_infor)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_infor['email']])

    def test_user_creation_no_email(self):
        """
        If we turn send email off, it should not send email after
        an user created.

        """
        new_user = RegistrationActivation.objects.create_inactive_user(send_email=False,
                                                                        **self.user_infor)
        self.assertEqual(len(mail.outbox), 0)

    def test_unexpired_user(self):
        """
        After user registration, if before the expiration date, user should not
        expired.

        """
        new_user = RegistrationActivation.objects.create_inactive_user(send_email=True,
                                                                       **self.user_infor)
        user_active = RegistrationActivation.objects.get(user=new_user)
        self.failIf(user_active.activation_key_expired())

    def test_expired_user(self):
        """
        If the user is not actived and outside the active window, user should
        expired.

        """
        new_user = RegistrationActivation.objects.create_inactive_user(send_email=True,
                                                                       **self.user_infor)
        new_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        new_user.save()
        user_active = RegistrationActivation.objects.get(user=new_user)
        self.failUnless(user_active.activation_key_expired())

    def test_valid_activation(self):
        """
        Test user using valid activation key to active the account. After user
        is activated, user.activation_key should be ACTIVATED defined in
        RegistrationActivation.

        """
        new_user = RegistrationActivation.objects.create_inactive_user(send_email=True,
                                                                       **self.user_infor)
        user_active = RegistrationActivation.objects.get(user=new_user)
        activated = RegistrationActivation.objects.activate_user(user_active.activation_key)

        self.failUnless(activated.is_active)
        self.assertEqual(activated.id, new_user.id)
        self.failUnless(activated.is_active)

        user_active = RegistrationActivation.objects.get(user=new_user)
        self.assertEqual(user_active.activation_key, RegistrationActivation.ACTIVATED)

    def test_activation_invalid_key(self):
        """
        Test user using invalid activation_key, should get False.

        """
        self.failIf(RegistrationActivation.objects.activate_user('invalid'))

    def test_activation_already_activated(self):
        """
        Test user using activation_key already used to activate.
        We should return False as an invalid activation.

        """

    def test_expired_user_deletion(self):
        new_user = RegistrationActivation.objects.create_inactive_user(send_email=True,
                                                                       **self.user_infor)
        expired_user = RegistrationActivation.objects.create_inactive_user(send_email=True,
                                                                           username='expired',
                                                                           password='123456',
                                                                           email='expired@example.com')
        expired_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        expired_user.save()
        RegistrationActivation.objects.delete_expiration_user()
        self.assertEqual(RegistrationActivation.objects.count(), 1)
        self.assertRaises(User.DoesNotExist, User.objects.get, username='expired')
