from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    recipients = models.ManyToManyField(User, related_name="messages_received")
    subject = models.CharField(max_length=150)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject
