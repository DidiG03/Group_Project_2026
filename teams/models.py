from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from organization.models import Department, TeamType

User = get_user_model()


class Team(models.Model):
    class TeamStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        RESTRUCTURED = "restructured", "Restructured"
        DISBANDED = "disbanded", "Disbanded"

    name = models.CharField(max_length=140, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="teams")
    team_type = models.ForeignKey(
        TeamType, on_delete=models.SET_NULL, null=True, blank=True, related_name="teams"
    )
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_teams")
    mission = models.TextField()
    responsibilities = models.TextField()
    contact_channel = models.CharField(max_length=200, help_text="Slack, Teams channel, or email.")
    repository_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=TeamStatus.choices, default=TeamStatus.RESTRUCTURED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def engineer_count(self):
        return self.members.count()

    def clean(self):
        if self.pk and self.status == Team.TeamStatus.ACTIVE and self.engineer_count < 5:
            raise ValidationError("An active team must have at least 5 engineers.")

    def save(self, *args, **kwargs):
        previous_status = None
        if self.pk:
            previous_status = Team.objects.filter(pk=self.pk).values_list("status", flat=True).first()
        self.full_clean()
        super().save(*args, **kwargs)
        if previous_status and previous_status != self.status:
            TeamStatusHistory.objects.create(
                team=self,
                old_status=previous_status,
                new_status=self.status,
            )

    def delete(self, *args, **kwargs):
        if self.department.teams.count() <= 3:
            raise ValidationError("Each department must keep at least 3 teams.")
        return super().delete(*args, **kwargs)


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    role = models.CharField(max_length=80, default="Engineer")
    skills = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("team", "email")
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.team.name})"

    def delete(self, *args, **kwargs):
        if self.team.status == Team.TeamStatus.ACTIVE and self.team.members.count() <= 5:
            raise ValidationError("An active team must keep at least 5 engineers.")
        return super().delete(*args, **kwargs)


class TeamDependency(models.Model):
    class RelationType(models.TextChoices):
        UPSTREAM = "upstream", "Upstream"
        DOWNSTREAM = "downstream", "Downstream"

    from_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="dependencies_from")
    to_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="dependencies_to")
    relation_type = models.CharField(max_length=20, choices=RelationType.choices)
    notes = models.CharField(max_length=250, blank=True)

    class Meta:
        unique_together = ("from_team", "to_team", "relation_type")
        ordering = ["from_team__name", "to_team__name"]

    def clean(self):
        if self.from_team_id == self.to_team_id:
            raise ValidationError("A team cannot depend on itself.")

    def __str__(self):
        return f"{self.from_team} -> {self.to_team} ({self.relation_type})"


class TeamStatusHistory(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="status_history")
    old_status = models.CharField(max_length=20, choices=Team.TeamStatus.choices)
    new_status = models.CharField(max_length=20, choices=Team.TeamStatus.choices)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.team.name}: {self.old_status} -> {self.new_status}"
