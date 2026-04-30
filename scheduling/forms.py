from django import forms

from core.form_helpers import apply_bootstrap_classes

from .models import Meeting


class MeetingForm(forms.ModelForm):
    scheduled_for = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Meeting
        fields = ["team", "title", "scheduled_for", "platform", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)
