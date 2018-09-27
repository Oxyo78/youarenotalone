from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from website.models import Interest, UserProfile, City, News

class AjaxTestCase(TestCase):
    """ URL test """
    fixtures = ['city.json', 'interest.json', 'user.json', 'userprofile.json', 'message.json']

    def setUp(self):
        self.client = Client()