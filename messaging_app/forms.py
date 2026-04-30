from django import forms
from django.contrib.auth import get_user_model

from core.form_helpers import apply_bootstrap_classes

from .models import Message

User = get_user_model()


class MessageForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ["recipients", "subject", "body", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)
