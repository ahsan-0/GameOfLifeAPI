from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from testingApp.seed_test_db import seed_test_db


# Create your tests here.
class PatternsGetRequestTests(APITestCase):
    patterns_url = reverse("test_get_patterns")

    def test_get_patterns(self):
        response = self.client.get(self.patterns_url)
        self.assertEqual(response.status_code, 200)
        patterns_list = response.data["patterns"]
        for pattern in patterns_list:
            keys = list(pattern.keys())
            self.assertEqual(
                keys, ["_id", "username", "pattern_name", "pattern_body", "created_at"]
            )

    def test_get_single_pattern(self):
        patterns = self.client.get(self.patterns_url).data["patterns"]
        first_pattern = patterns[0]
        url_inc_id = reverse("test_get_single_pattern", args=[first_pattern["_id"]])
        response = self.client.get(url_inc_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_pattern.items() <= response.data.items(), True)
        self.assertEqual(
            list(response.data.keys()),
            ["_id", "username", "pattern_name", "pattern_body", "created_at"],
        )

    def test_get_nonexistent_pattern(self):
        url_inc_id = reverse("test_get_single_pattern", args=["9328432234"])
        response = self.client.get(url_inc_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "Request contains invalid id.")


class PatternsPostRequestTests(APITestCase):
    patterns_url = reverse("test_get_patterns")

    def test_post_pattern(self):
        seed_test_db()
        request_body = {
            "username": "bob12",
            "pattern_name": "special pattern",
            "pattern_body": "0101001101 1011001010 0011011010 1000101010 0100101000 1101100000 1010000011 1111000000 0100101010 0000101010",
        }
        response = self.client.post(self.patterns_url, request_body, format="json")
        new_pattern = response.data["pattern"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(request_body.items() <= new_pattern.items(), True)
        patterns = self.client.get(self.patterns_url).data["patterns"]
        self.assertEqual(new_pattern in patterns, True)

    def test_post_nonexistent_pattern(self):
        request_body = {
            "username": "nonexistentUser",
            "pattern_name": "special pattern",
            "pattern_body": "0101001101 1011001010 0011011010 1000101010 0100101000 1101100000 1010000011 1111000000 0100101010 0000101010",
        }
        response = self.client.post(self.patterns_url, request_body, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "User does not exist.")

    def test_post_invalid_prop(self):
        request_body = {
            "username": "bob12",
            "pattern_names": "special pattern",
            "pattern_body": "0101001101 1011001010 0011011010 1000101010 0100101000 1101100000 1010000011 1111000000 0100101010 0000101010",
        }
        response = self.client.post(self.patterns_url, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Request body contains invalid key.")

    def test_post_missing_prop(self):
        request_body = {"username": "bob12"}
        response = self.client.post(self.patterns_url, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["msg"], "Request body is missing a required key."
        )

    def test_post_duplicate_pattern(self):
        seed_test_db()
        request_body = {
            "username": "bob12",
            "pattern_name": "special pattern",
            "pattern_body": "0101001101 1011001010 0011011010 1000101010 0100101000 1101100000 1010000011 1111000000 0100101010 0000101010",
        }
        response = self.client.post(self.patterns_url, request_body, format="json")
        response = self.client.post(self.patterns_url, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Pattern already exists in database.")


class PatternsPutRequestTest(APITestCase):
    def test_put_new_pattern_name(self):
        request_body = {"pattern_name": "icecrystal"}
        patterns = self.client.get("/test/patterns").data["patterns"]
        first_pattern = patterns[0]
        url_inc_id = reverse("test_get_single_pattern", args=[first_pattern["_id"]])
        response = self.client.put(url_inc_id, request_body, format="json")
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["updated_pattern"]["pattern_name"], "icecrystal")
        first_pattern.pop("pattern_name")
        self.assertEqual(
            all(
                response.data["updated_pattern"].get(k) == v
                for k, v in first_pattern.items()
            ),
            True,
        )

    def test_put_nonexistent_user(self):
        request_body = {"pattern_name": "icecrystal"}
        response = self.client.put(
            "/test/patterns/293896324", request_body, format="json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "Request contains invalid id.")

    def test_put_missing_key(self):
        request_body = {"pattern_nam": "icecrystal"}
        patterns = self.client.get("/test/patterns").data["patterns"]
        first_pattern = patterns[0]
        url_inc_id = reverse("test_get_single_pattern", args=[first_pattern["_id"]])
        response = self.client.put(url_inc_id, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Request is missing required property")

    def test_put_empty_request(self):
        request_body = {}
        patterns = self.client.get("/test/patterns").data["patterns"]
        first_pattern = patterns[0]
        url_inc_id = reverse("test_get_single_pattern", args=[first_pattern["_id"]])
        response = self.client.put(url_inc_id, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Request body cannot be empty")

    def test_put_invalid_prop(self):
        request_body = {"pattern_name": "icecrystal", "username": "jolly56"}
        patterns = self.client.get("/test/patterns").data["patterns"]
        first_pattern = patterns[0]
        url_inc_id = reverse("test_get_single_pattern", args=[first_pattern["_id"]])
        response = self.client.put(url_inc_id, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Request contains invalid property.")


class ItemsDeleteRequestTest(APITestCase):
    def test_delete_patterns(self):
        seed_test_db()
        patterns = self.client.get(reverse("test_get_patterns")).data["patterns"]
        first_pattern = patterns[0]
        url_inc_id = reverse("test_get_single_pattern", args=[first_pattern["_id"]])
        response = self.client.delete(url_inc_id)
        self.assertEqual(response.status_code, 204)
        patterns = self.client.get(reverse("test_get_patterns")).data["patterns"]
        self.assertEqual(first_pattern in patterns, False)

        response = self.client.delete(url_inc_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "Request contains invalid id.")

        response = self.client.get(url_inc_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "Request contains invalid id.")

    def test_delete_users(self):
        seed_test_db()
        users = self.client.get(reverse("test_get_users")).data["users"]
        first_user = users[0]
        url_inc_id = reverse("test_get_single_user", args=[first_user["_id"]])
        response = self.client.delete(url_inc_id)
        self.assertEqual(response.status_code, 204)
        users = self.client.get(reverse("test_get_users")).data["users"]
        self.assertEqual(first_user in users, False)

        response = self.client.delete(url_inc_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "Request contains invalid id.")

        response = self.client.get(url_inc_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "Request contains invalid id.")


class UsersGetRequestTests(APITestCase):
    users_url = reverse("test_get_users")

    def test_get_users(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, 200)
        users_list = response.data["users"]
        for user in users_list:
            keys = list(user.keys())
            self.assertEqual(
                keys, ["_id", "account_owner", "username", "email", "avatar_url"]
            )

    def test_get_single_user(self):
        users = self.client.get(self.users_url).data["users"]
        first_user = users[0]
        url_inc_id = reverse("test_get_single_user", args=[first_user["_id"]])
        response = self.client.get(url_inc_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_user.items() <= response.data.items(), True)
        self.assertEqual(
            list(response.data.keys()),
            ["_id", "account_owner", "username", "email", "avatar_url"],
        )

    def test_get_nonexistent_user(self):
        url_inc_id = reverse("test_get_single_user", args=["63d18dec7200a847c7d9e6b7"])
        response = self.client.get(url_inc_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "Request contains invalid id.")


class UsersPostRequestTests(APITestCase):
    users_url = reverse("test_get_users")

    def test_post_user(self):
        seed_test_db()
        request_body = {
            "account_owner": "Jarvis Ray",
            "username": "jr98878",
            "email": "a987ss@outlook.com",
            "avatar_url": "https://www.bcito.com/url?",
        }
        response = self.client.post(self.users_url, request_body, format="json")
        new_user = response.data["user"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(request_body.items() <= new_user.items(), True)
        users = self.client.get(self.users_url).data["users"]
        self.assertEqual(new_user in users, True)

        response = self.client.post(self.users_url, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "User already exists in database.")

    def test_post_invalid_prop(self):
        request_body = {
            "account_owners": "Bob Carlton",
            "username": "jjbc384",
            "email": "a987ss@outlook.com",
            "avatar_url": "https://www.bcito.com/url?",
        }
        response = self.client.post(self.users_url, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Request body contains invalid key.")

        request_body = {
            "account_owner": "Bob Carlton",
            "username": "jjbc384",
            "email": "a987ss@outlook.com",
            "avatar_url": "https://www.bcito.com/url?",
            "age": 433,
        }

        response = self.client.post(self.users_url, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Request body contains invalid key.")

    def test_post_missing_prop(self):
        request_body = {
            "username": "allity",
            "email": "jsop98@outlook.com",
            "avatar_url": "https://www.bcito.com/url?",
        }
        response = self.client.post(self.users_url, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["msg"], "Request body is missing a required key."
        )

    def test_post_taken_username(self):
        request_body = {
            "account_owner": "Jamal Reyes",
            "username": "lornBG",
            "email": "23asds@outlook.com",
            "avatar_url": "https://www.bcito.com/url?",
        }
        response = self.client.post(self.users_url, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "That username is already taken.")


class UsersPutRequestTests(APITestCase):
    def test_put_user(self):
        seed_test_db()
        request_body = {
            "account_owner": "Joel Hurst",
            "username": "BINGO445",
            "email": "bigjoel445@outlook.com",
            "avatar_url": "www.newavatars.com/avatar",
        }

        users = self.client.get("/test/users").data["users"]
        first_user = users[0]
        url_inc_id = reverse("test_get_single_user", args=[first_user["_id"]])
        response = self.client.put(url_inc_id, request_body, format="json")
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["updated_user"]["username"], "BINGO445")
        self.assertEqual(
            all(
                response.data["updated_user"].get(k) == v
                for k, v in request_body.items()
            ),
            True,
        )

    def test_put_nonexistent_user(self):
        request_body = {
            "account_owner": "Django Mongo Djongo",
        }
        response = self.client.put(
            "/test/users/63d1ce82c46f7zu09c93201e", request_body, format="json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "Request contains invalid id.")

    def test_put_invalid_username(self):
        request_body = {"username": "BINGO 445"}
        users = self.client.get("/test/users").data["users"]
        first_user = users[0]
        url_inc_id = reverse("test_get_single_user", args=[first_user["_id"]])
        response = self.client.put(url_inc_id, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Username cannot contain spaces.")

    def test_put_invalid_key(self):
        request_body = {"favourite_colour": "red"}
        users = self.client.get("/test/users").data["users"]
        first_user = users[0]
        url_inc_id = reverse("test_get_single_user", args=[first_user["_id"]])
        response = self.client.put(url_inc_id, request_body, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Request body contains invalid key.")

    def test_put_empty_request(self):
        users = self.client.get("/test/users").data["users"]
        first_user = users[0]
        url_inc_id = reverse("test_get_single_user", args=[first_user["_id"]])
        response = self.client.put(url_inc_id, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["msg"], "Request cannot be an empty object")


class PatternsByUserTests(APITestCase):
    def test_get_patterns_by_username(self):
        url_inc_username = reverse("test_get_patterns_by_username", args=["zack81"])
        response = self.client.get(url_inc_username)
        self.assertEqual(response.status_code, 200)
        for pattern in response.data["patterns"]:
            self.assertEqual(pattern["username"], "zack81")

    def test_invalid_username(self):
        url_inc_username = reverse("test_get_patterns_by_username", args=["bollydolly"])
        response = self.client.get(url_inc_username)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "User does not exist.")

    def test_no_patterns(self):
        url_inc_username = reverse("test_get_patterns_by_username", args=["BM"])
        response = self.client.get(url_inc_username)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["msg"], "There are no patterns for that user.")
