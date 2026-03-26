from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from organization.models import Department
from teams.models import Team


class ReportsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reportuser", password="StrongPass123!")
        department = Department.objects.create(
            name="Reports Department",
            leader_name="Lead Person",
            specialisation="Operations",
        )
        Team.objects.create(
            name="Reports Team",
            department=department,
            manager=self.user,
            mission="Mission",
            responsibilities="Responsibilities",
            contact_channel="#reports-team",
        )

    def test_reports_page_requires_login(self):
        response = self.client.get(reverse("reports_home"))
        self.assertEqual(response.status_code, 302)

    def test_csv_export(self):
        self.client.login(username="reportuser", password="StrongPass123!")
        response = self.client.get(reverse("report_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
