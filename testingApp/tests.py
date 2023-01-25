from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from testingApp.seed_test_db import seed_test_db


# Create your tests here.
class PatternsGetRequestTests(APITestCase):
    patterns_url = reverse('test_get_patterns')
    def test_get_patterns(self):
        response = self.client.get(self.patterns_url)
        self.assertEqual(response.status_code, 200)
        patterns_list = response.data['patterns']
        for pattern in patterns_list:
            keys = list(pattern.keys())
            self.assertEqual(keys, ['_id', 'username', 'pattern_name', 'pattern_body', 'created_at'])
    
    def test_get_single_pattern(self):
        patterns = self.client.get(self.patterns_url).data['patterns']
        first_pattern = patterns[0]
        url_inc_id = reverse('test_get_single_pattern', args=[first_pattern['_id']])
        response = self.client.get(url_inc_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_pattern.items() <= response.data.items(), True)
        self.assertEqual(list(response.data.keys()), ['_id', 'username', 'pattern_name', 'pattern_body', 'created_at'])
    
    def test_get_nonexistent_pattern(self):
        url_inc_id = reverse('test_get_single_pattern', args=['9328432234'])
        response = self.client.get(url_inc_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['msg'], "Request contains invalid id.")


class PatternsPostRequestTests(APITestCase):
    patterns_url = reverse('test_get_patterns')
    def test_post_pattern(self):
        request_body = {
			"username": "bob12",
			"pattern_name": "special pattern",
			"pattern_body": "0101001101 1011001010 0011011010 1000101010 0100101000 1101100000 1010000011 1111000000 0100101010 0000101010",
	    }
        response = self.client.post(self.patterns_url, request_body, format='json')
        new_pattern = response.data["pattern"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(request_body.items() <= new_pattern.items(), True)
        patterns = self.client.get(self.patterns_url).data['patterns']
        self.assertEqual(new_pattern in patterns, True)


    def test_post_nonexistent_user(self):
        request_body = {
			"username": "nonexistentUser",
			"pattern_name": "special pattern",
			"pattern_body": "0101001101 1011001010 0011011010 1000101010 0100101000 1101100000 1010000011 1111000000 0100101010 0000101010",
	    }
        response = self.client.post(self.patterns_url, request_body, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['msg'], "User does not exist.")
    

    def test_post_invalid_prop(self):
        request_body = {
			"username": "bob12",
			"pattern_names": "special pattern",
			"pattern_body": "0101001101 1011001010 0011011010 1000101010 0100101000 1101100000 1010000011 1111000000 0100101010 0000101010",
	    }
        response = self.client.post(self.patterns_url, request_body, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['msg'], "Request body contains invalid key.")


    def test_post_missing_prop(self):
        request_body = { "username": "bob12" }
        response = self.client.post(self.patterns_url, request_body, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['msg'], "Request body is missing a required key.")

    
