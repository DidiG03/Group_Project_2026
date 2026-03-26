from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from organization.models import Department, TeamType
from teams.models import Team, TeamDependency, TeamMember


class Command(BaseCommand):
    help = "Seed sample data to satisfy coursework minimum dataset rules."

    def handle(self, *args, **options):
        manager_1, _ = User.objects.get_or_create(
            username="manager1",
            defaults={
                "first_name": "Ava",
                "last_name": "Turner",
                "email": "ava.turner@example.com",
            },
        )
        manager_1.set_password("Password123!")
        manager_1.save()

        manager_2, _ = User.objects.get_or_create(
            username="manager2",
            defaults={
                "first_name": "Noah",
                "last_name": "Patel",
                "email": "noah.patel@example.com",
            },
        )
        manager_2.set_password("Password123!")
        manager_2.save()

        backend, _ = Department.objects.get_or_create(
            name="Platform Engineering",
            defaults={"leader_name": "Chris Evans", "specialisation": "Backend Services"},
        )
        product, _ = Department.objects.get_or_create(
            name="Product Engineering",
            defaults={"leader_name": "Sophia Lewis", "specialisation": "Customer Products"},
        )

        service_type, _ = TeamType.objects.get_or_create(name="Service Team")
        enablement_type, _ = TeamType.objects.get_or_create(name="Enablement Team")

        departments = [(backend, manager_1), (product, manager_2)]
        created_teams = []
        for department, manager in departments:
            for index in range(1, 4):
                team, _ = Team.objects.get_or_create(
                    name=f"{department.name.split()[0]} Team {index}",
                    defaults={
                        "department": department,
                        "team_type": service_type if index % 2 else enablement_type,
                        "manager": manager,
                        "mission": "Deliver reliable software products and services.",
                        "responsibilities": "Build, maintain and support key services.",
                        "contact_channel": f"#{department.name.split()[0].lower()}-team-{index}",
                        "repository_url": "https://github.com/example/repository",
                    },
                )
                created_teams.append(team)
                for engineer_index in range(1, 6):
                    TeamMember.objects.get_or_create(
                        team=team,
                        email=f"{team.name.lower().replace(' ', '.')}.eng{engineer_index}@example.com",
                        defaults={
                            "full_name": f"Engineer {engineer_index} {team.name}",
                            "role": "Engineer",
                            "skills": "Python, Django, SQL",
                        },
                    )
                if team.status != Team.TeamStatus.ACTIVE:
                    team.status = Team.TeamStatus.ACTIVE
                    team.save()

        for idx in range(len(created_teams) - 1):
            TeamDependency.objects.get_or_create(
                from_team=created_teams[idx],
                to_team=created_teams[idx + 1],
                relation_type=TeamDependency.RelationType.DOWNSTREAM,
            )

        self.stdout.write(self.style.SUCCESS("Sample data seeded successfully."))
