from django.db import models
from django.contrib.auth import get_user_model

from teams.models import Team

User = get_user_model()


class Meeting(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="meetings")
    title = models.CharField(max_length=140)
    scheduled_for = models.DateTimeField()
    platform = models.CharField(max_length=120, help_text="e.g. Teams, Zoom")
    message = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="meetings_created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_for"]

    def __str__(self):
        return f"{self.title} - {self.team.name}"
