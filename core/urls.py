from django.urls import path

from .views import DashboardView, MarkNotificationReadView, NotificationListView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("notifications/<int:pk>/read/", MarkNotificationReadView.as_view(), name="notification_read"),
]
