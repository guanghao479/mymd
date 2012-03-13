from django.test import TestCase
from django.core.urlresolvers import reverse
from registration.models import RegistrationActivation

class HomePageViewTest(TestCase):
    user_infor = {'username': 'example',
                       'password': '123456',
                       'email': 'example@example.com'}
    def setUp(self):
        """
        Set up a user and make it as active.
        """
        self.user = RegistrationActivation.objects.create_inactive_user(**self.user_infor)
        self.user.is_active = True;

    def test_home_redirect_without_login(self):
        """
        Home page should redirected to login page if user is not authenticated.
        """
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200
)

    def test_home_with_login(self):
        """
        Page should get status code 200 with user authenticated.
        """
        self.user.set_password('123456')
        self.user.save()
        login_status = self.client.login(username='example', password='123456')
        self.failIf(not login_status)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
