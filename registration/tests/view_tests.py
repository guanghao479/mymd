from django.test import TestCase
from django.core.urlresolvers import reverse
from registration.models import RegistrationActivation

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
        
class LoginViewTestCases(TestCase):
    
    user_infor = {'username': 'example',
                  'email': 'example@example.com',
                  'password': '123456'}
    
    def test_success_Login(self):
        """Test user successfully login using correct username and password"""
        new_user = RegistrationActivation.objects.create_inactive_user(**self.user_infor)
        new_user.is_active = True;
        response = self.client.post(reverse('login'), {'username': 'example',
                                                       'password': '123456'})
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)