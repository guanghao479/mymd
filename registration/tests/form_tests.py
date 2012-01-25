from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from registration.models import RegistrationActivation
from django.contrib.auth import authenticate

from registration import forms

class RegistrationFormTestCases(TestCase):
    """
    Test cases for Registration form.

    """

    def test_failure_register_with_empty_username(self):
        """
        Register should fail and remain on the same page,
        with empty username.

        """
        response = self.client.post(reverse('register'), {'username': '',
                                                          'email1': 'example@eee.com',
                                                          'email2': 'example@eee.com',
                                                          'password': '123445'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'username',
                             errors=u'This field is required.')

    def test_failure_register_with_wrong_email_format(self):
        """
        Register should fail and remain on the same page
        with wrong email format.

        """
        response = self.client.post(reverse('register'), {'username': 'example',
                                                          'email1': 'example',
                                                          'email2': 'example@eee.com',
                                                          'password': '123445'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email1',
                             errors=u'Enter a valid e-mail address.')

    def test_failure_register_with_unmatched_email(self):
        """
        Register should fail and remain on the same page
        with wrong email format.

        """
        response = self.client.post(reverse('register'), {'username': 'example1',
                                                          'email1': 'example@eee1.com',
                                                          'email2': 'example@eee.com',
                                                          'password': '123445'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None,
                             errors=u"The two email fields didn't match.")
        self.assertEqual(RegistrationActivation.objects.count(), 0)
