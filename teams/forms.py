from django import forms

from core.form_helpers import apply_bootstrap_classes

from .models import Team, TeamDependency, TeamMember


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "name",
            "department",
            "team_type",
            "manager",
            "mission",
            "responsibilities",
            "contact_channel",
            "repository_url",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        instance = self.instance
        if status == Team.TeamStatus.ACTIVE:
            if not instance.pk:
                raise forms.ValidationError(
                    "Create the team first, add at least 5 engineers, then set status to Active."
                )
            if instance.engineer_count < 5:
                raise forms.ValidationError("An active team must have at least 5 engineers.")
        return cleaned_data


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["team", "full_name", "email", "role", "skills"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)


class TeamDependencyForm(forms.ModelForm):
    class Meta:
        model = TeamDependency
        fields = ["from_team", "to_team", "relation_type", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)
