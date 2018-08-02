from django.test import TestCase
from django.test import Client


class UrlTestCase(TestCase):
    """ URL test """

    def setUp(self):
        self.client = Client()

    def test_url(self):
        home = self.client.get('')

        self.assertEqual(home.status_code, 200)
