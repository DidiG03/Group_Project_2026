from django.urls import path

from .views import AuditLogListView, DashboardView, MarkNotificationReadView, NotificationListView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("notifications/<int:pk>/read/", MarkNotificationReadView.as_view(), name="notification_read"),
    path("audit-log/", AuditLogListView.as_view(), name="audit_log"),
]
