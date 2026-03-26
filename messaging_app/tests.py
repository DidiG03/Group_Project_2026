from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from core.models import Notification


class MessagingTests(TestCase):
    def test_sent_message_creates_notification(self):
        sender = User.objects.create_user(username="sender", password="StrongPass123!")
        receiver = User.objects.create_user(username="receiver", password="StrongPass123!")
        self.client.login(username="sender", password="StrongPass123!")
        response = self.client.post(
            reverse("message_create"),
            {
                "recipients": [receiver.pk],
                "subject": "Test",
                "body": "Body",
                "status": "sent",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Notification.objects.filter(user=receiver).count(), 1)
