from datetime import date

from django.test import TestCase

from meetup.models import Meetup, Attend
from city.models import City
from django.contrib.auth.models import User

class MeetupTestCase(TestCase):

    def setUp(self):
        self.city = City.objects.create(country='China', name='Beijing', size=100)
        self.organizer = User.objects.create_user(username='Xinghan', email='xinghan@email.com')
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

    def test_meetup_model(self):
        """
        Tests for meetup model.

        """
        self.assertEquals(Meetup.objects.all().count(), 1)
        self.assertEquals(self.meetup.title, 'loveandhelp group discussion')
        self.assertEquals(self.meetup.content, 'loveandhelp group discussion')
        self.assertEquals(self.meetup.city.name, 'Beijing')
        self.assertEquals(self.meetup.organizer.username, 'Xinghan')
        self.assertEquals(self.meetup.address, 'Yayuncun, starbucks')
        self.assertEquals(self.meetup.date, date(2012, 10,12))
        self.assertEquals(self.meetup.created_date, date(2012, 10, 9))
        self.assertEquals(self.meetup.modified_date, date(2012, 10, 9))

    def test_meetup_attend(self):
        """
        Test cases for meetup attend model.

        """
        self.attender1 = User.objects.create_user(username='Lucy', email='lucy@email.com')
        self.attender2 = User.objects.create_user(username='Guanghao', email='guanghao@email.com')
        self.attend_relationship = Attend.objects.create(attender = self.attender1,
                                                    meetup = self.meetup,
                                                    attend_date = date(2012, 10, 13))
        self.assertEquals(self.attend_relationship.attender.username, 'Lucy')
        self.assertEquals(self.attend_relationship.meetup.title, 'loveandhelp group discussion')
        self.assertEquals(self.attend_relationship.attend_date, date(2012, 10, 13))
        self.assertTrue(Attend.objects.is_attendee(self.attender1, self.meetup))
        self.assertFalse(Attend.objects.is_attendee(self.attender2, self.meetup))



