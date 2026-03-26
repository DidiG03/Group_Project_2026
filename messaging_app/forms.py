from django import forms
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()


class MessageForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ["recipients", "subject", "body", "status"]
