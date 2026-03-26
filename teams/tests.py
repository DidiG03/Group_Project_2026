from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from organization.models import Department

from .models import Team, TeamMember


class TeamTests(TestCase):
    def test_team_can_be_created(self):
        manager = User.objects.create_user(username="manager", password="StrongPass123!")
        department = Department.objects.create(
            name="Engineering",
            leader_name="Lead Name",
            specialisation="Delivery",
        )
        team = Team.objects.create(
            name="Core Team",
            department=department,
            manager=manager,
            mission="Mission text",
            responsibilities="Responsibilities text",
            contact_channel="#core-team",
        )
        self.assertEqual(team.name, "Core Team")

    def test_active_team_requires_five_engineers(self):
        manager = User.objects.create_user(username="manager2", password="StrongPass123!")
        department = Department.objects.create(
            name="Engineering 2",
            leader_name="Lead Name",
            specialisation="Delivery",
        )
        team = Team.objects.create(
            name="Infra Team",
            department=department,
            manager=manager,
            mission="Mission text",
            responsibilities="Responsibilities text",
            contact_channel="#infra-team",
            status=Team.TeamStatus.RESTRUCTURED,
        )
        TeamMember.objects.create(team=team, full_name="A", email="a@example.com")
        TeamMember.objects.create(team=team, full_name="B", email="b@example.com")
        TeamMember.objects.create(team=team, full_name="C", email="c@example.com")
        TeamMember.objects.create(team=team, full_name="D", email="d@example.com")

        team.status = Team.TeamStatus.ACTIVE
        with self.assertRaises(ValidationError):
            team.save()
