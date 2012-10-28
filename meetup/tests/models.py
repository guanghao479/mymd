from datetime import date

from django.test import TestCase

from meetup.models import Meetup
from city.models import City
from django.contrib.auth.models import User

class MeetupTestCase(TestCase):

    def setUp(self):
        self.city = City.objects.create(country='China', name='Beijing', size=100)
        self.organizer = User.objects.create_user(username='Xinghan', email='xinghan@gmail.com')
        self.address = 'Yayuncun, starbucks'
        self.hold_date = date(2012, 10,12)
        self.title = 'loveandhelp group discussion'
        self.content = 'loveandhelp group discussion'
        self.created_date = date(2012, 10, 9)
        self.modified_date = date(2012, 10, 9)
        self.meetup = Meetup.objects.create(organizer = self.organizer,
                                       city = self.city,
                                       address = self.address,
                                       date = self.hold_date,
                                       title = self.title,
                                       content = self.content,
                                       created_date = self.created_date,
                                       modified_date = self.modified_date)

    def test_meetup(self):
        """
        Tests for meetup model.

        """
        self.assertEquals(Meetup.objects.all().count(), 1)
        self.assertEquals(self.meetup.title, 'loveandhelp group discussion')
        self.assertEquals(self.meetup.city.name, 'Beijing')
        


