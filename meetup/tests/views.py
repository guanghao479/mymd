from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from meetup.models import Meetup
from city.models import City
from meetup.forms import MeetupForm



class MeetupViewTests(TestCase):
    """
    Test meetup views.

    """

    def test_meetup_create_view_initial(self):
        """
        Test meetup creation view response.

        """
        response = self.client.get(reverse('meetup:meetup_create'))
        self.assertEqual(response.status_code, 302)
        #self.assertTemplateUsed(response, 'meetup/meetup_create.html/')

    def test_meetup_create_view_success(self):
        """
        Test successfully create meetup.

        """
        pass
        #view = meetup.view.MeetupCreateView()

