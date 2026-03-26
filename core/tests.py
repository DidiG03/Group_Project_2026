from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Notification


class CoreTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_renders_for_logged_in_user(self):
        User.objects.create_user(username="coreuser", password="StrongPass123!")
        self.client.login(username="coreuser", password="StrongPass123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_notifications_page_loads(self):
        user = User.objects.create_user(username="noticeuser", password="StrongPass123!")
        Notification.objects.create(user=user, title="Hello")
        self.client.login(username="noticeuser", password="StrongPass123!")
        response = self.client.get(reverse("notifications"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_has_no_cache_headers_for_logged_in_user(self):
        User.objects.create_user(username="cacheuser", password="StrongPass123!")
        self.client.login(username="cacheuser", password="StrongPass123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("no-store", response["Cache-Control"])

    def test_unknown_route_uses_custom_404_page(self):
        response = self.client.get("/brxihi")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Page not found", status_code=404)
