from django.test import TestCase
from django.test.client import Client


class FeedsTest(TestCase):
    fixtures = ['feeds']

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_section(self):
        response = self.client.get('/section/1')
        self.assertEqual(response.status_code, 200)

    def test_feed(self):
        response = self.client.get('/feed/1')
        self.assertEqual(response.status_code, 200)
