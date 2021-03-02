from django.http import response
from django.test import TestCase, Client
from django.contrib.auth.models import User
import json
# Create your tests here.

class UserTest(TestCase):

    client = Client()

    def setUp(self):
        user = User.objects.create(
            username = "test123",
            password = "testpassword1020",
        )

    def test_login_success(self):

        data = {
            "username" : "test123",
            "password" : "testpassword1020",
        }

        response = self.client.post("/rest-auth/login/", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code,200)