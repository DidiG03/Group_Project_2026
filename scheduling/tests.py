from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from core.models import Notification
from organization.models import Department
from teams.models import Team


class SchedulingTests(TestCase):
    def test_meeting_creates_manager_notification(self):
        creator = User.objects.create_user(username="creator", password="StrongPass123!")
        manager = User.objects.create_user(username="mgr", password="StrongPass123!")
        department = Department.objects.create(name="DepX", leader_name="Lead", specialisation="Core")
        team = Team.objects.create(
            name="Sched Team",
            department=department,
            manager=manager,
            mission="Mission",
            responsibilities="Resp",
            contact_channel="#sched-team",
        )
        self.client.login(username="creator", password="StrongPass123!")
        response = self.client.post(
            reverse("meeting_create"),
            {
                "team": team.pk,
                "title": "Planning",
                "scheduled_for": (timezone.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
                "platform": "Teams",
                "message": "Plan work",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Notification.objects.filter(user=manager).count(), 1)
