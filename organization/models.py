from django.db import models
from django.core.exceptions import ValidationError


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    leader_name = models.CharField(max_length=120)
    specialisation = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if Department.objects.count() <= 2:
            raise ValidationError("At least two departments must remain in the system.")
        return super().delete(*args, **kwargs)


class TeamType(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
