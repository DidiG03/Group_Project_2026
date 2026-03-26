from django.urls import path

from .views import MeetingCreateView, MeetingDeleteView, MeetingListView, MeetingUpdateView

urlpatterns = [
    path("", MeetingListView.as_view(), name="meeting_list"),
    path("new/", MeetingCreateView.as_view(), name="meeting_create"),
    path("<int:pk>/edit/", MeetingUpdateView.as_view(), name="meeting_update"),
    path("<int:pk>/delete/", MeetingDeleteView.as_view(), name="meeting_delete"),
]
