from django.urls import path

from .views import DraftView, InboxView, MessageCreateView, MessageDeleteView, SentView

urlpatterns = [
    path("inbox/", InboxView.as_view(), name="inbox"),
    path("sent/", SentView.as_view(), name="sent"),
    path("draft/", DraftView.as_view(), name="draft"),
    path("new/", MessageCreateView.as_view(), name="message_create"),
    path("<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
]
