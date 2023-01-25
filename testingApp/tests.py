from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from testingApp.seed_test_db import seed_test_db



# Create your tests here.
class PatternsAPIViewTests(APITestCase):
    patterns_url = reverse('test_get_patterns')
    def test_get_patterns(self):
        #seed_test_db()
        response = self.client.get(self.patterns_url)
        self.assertEqual(response.status_code, 200)