from django.test import TestCase
from django.core.urlresolvers import reverse
from registration.models import RegistrationActivation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationViewTestCases(TestCase):
    fixtures = ['registration_views_testdata.json']

    def test_success_registeration_status_code(self):
        """register page should 200 response."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_registeration_template(self):
        """Test GET registration uses the correct template"""
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_registration_template_contain(self):
        """Test GET registration template has the correct contain"""
        response = self.client.get(reverse('register'))
        self.assertContains(response, "Register", count=1, status_code=200)

    def test_success_register(self):
        """
        Register POST should success with the correct
        email and password.

        """
        response = self.client.post(reverse('register'), {'username': 'example',
                                                          'email1': 'example@eee.com',
                                                          'email2': 'example@eee.com',
                                                          'password': '123445'})
        self.assertEqual(RegistrationActivation.objects.count(), 1)
        self.assertRedirects(response, reverse('needs_activation'),
                             status_code=302, target_status_code=200)



class LoginViewTestCases(TestCase):

    def setUp(self):
        self.new_user = RegistrationActivation.objects.create_inactive_user(**self.user_infor)
    user_infor = {'username': 'example',
                  'email': 'example@example.com',
                  'password': '123456'}

    def test_success_create_user(self):
        """
        Test user successfully login using correct username and password.
        User should redirected to home page, and status code should be 302.
        """
        self.new_user.is_active = True;
        self.assertEqual(self.new_user.username, 'example')
        self.assertEqual(self.new_user.email, 'example@example.com')
        self.failUnless(self.new_user.check_password('123456'))
        self.failIf(not self.new_user.is_active)
        saved_user = User.objects.get(email__iexact='example@example.com')
        self.assertIsNotNone(saved_user)
        login_user = authenticate(username='example', password='123456')
        self.assertIsNotNone(login_user)



    def test_success_login_with_username(self):
        """
        Test user successfully login using username.
        Page should redirected to index.
        """
        response = self.client.post(reverse('login'), {'username': 'example',
                                                       'password': '123456'})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_success_login_with_email(self):
        """
        Test user successfully login using email.
        Page should redirected to index.
        """
        response = self.client.post(reverse('login'), {'username': 'example@example.com',
                                                       'password': '123456'})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_render_homepage_with_login_user_login_again(self):
        """
        When login user try to access login view again, we should just
        render home page.

        """
        self.client.post(reverse('login'), {'username': 'example@example.com',
                                                       'password': '123456'})
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'home/home.html')

    def test_user_login_fail_with_wrong_password(self):
        """
        Test user fail login using wrong password.
        Page should generates login page.
        """
        response = self.client.post(reverse('login'), {'username': 'example',
                                                       'password': '1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_login_fail_with_wrong_password(self):
        """
        Test user fail login using wrong username.
        Page should generates login page.
        """
        response = self.client.post(reverse('login'), {'username': 'example2',
                                                       'password': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_logout_succeed(self):
        self.client.post(reverse('login'), {'username': 'example',
                                            'password': '123456'})
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)
