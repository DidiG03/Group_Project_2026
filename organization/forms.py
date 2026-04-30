from django import forms

from core.form_helpers import apply_bootstrap_classes

from .models import Department, TeamType


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "leader_name", "specialisation", "description", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)


class TeamTypeForm(forms.ModelForm):
    class Meta:
        model = TeamType
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)
