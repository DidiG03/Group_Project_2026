from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from organization.models import Department
from teams.models import Team


class AnalyticsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="analyticsuser", password="StrongPass123!")
        department = Department.objects.create(
            name="Analytics Department",
            leader_name="Leader",
            specialisation="Data",
        )
        Team.objects.create(
            name="Analytics Team",
            department=department,
            manager=self.user,
            mission="Mission",
            responsibilities="Responsibilities",
            contact_channel="#analytics-team",
        )

    def test_charts_page_loads_for_logged_in_user(self):
        self.client.login(username="analyticsuser", password="StrongPass123!")
        response = self.client.get(reverse("charts"))
        self.assertEqual(response.status_code, 200)
