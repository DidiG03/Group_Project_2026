from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        User.objects.create_user(username="testuser", password="StrongPass123!")
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "StrongPass123!"})
        self.assertEqual(response.status_code, 302)
