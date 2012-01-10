from django.contrib.auth.models import User
from registration.models import RegistrationActivation
from django.test import TestCase
from django.core import mail
import re

class RegistrationModelTestCases(TestCase):
    """
    Test the registration model including RegistrationManager
    RegistrationProfile and RegistrationActivation.
    
    """
    user_infor = {'username': 'example',
                  'email': 'example@example.com',
                  'password': '123456'}
    
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
        new_user = RegistrationActivation.objects.create_inactive_user(**self.user_infor)
        self.assertEqual(len(mail.outbox), 1)
        
    def test_user_creation_no_email(self):
        """
        If we turn send email off, it should not send email after
        an user created.
        
        """
        new_user = RegistrationActivation.objects.create_inactive_user(send_email=False,
                                                                        **self.user_infor)
        self.assertEqual(len(mail.outbox), 0)
        
    
        