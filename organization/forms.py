from django import forms

from .models import Department, TeamType


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "leader_name", "specialisation", "description", "is_active"]


class TeamTypeForm(forms.ModelForm):
    class Meta:
        model = TeamType
        fields = ["name", "description"]
