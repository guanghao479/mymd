"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

class AvailabilityTest(TestCase):
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200) 

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
    
    def test_activate(self):
        response = self.client.get('/activate/')
        self.assertEqual(response.status_code, 200)
        
    def test_password_change(self):
        # Need to log in first
        response = self.client.get('/password_change/')
        self.assertEqual(response.status_code, 200)
        
    def test_password_reset(self):
        # Need to log in first
        response = self.client.get('/password_reset/')
        self.assertEqual(response.status_code, 200)
        
    def test_logout(self):
        # Need to log in first
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        
    def test_user_home(self):
        # Need to log in first
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)
        
        
