from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "team", "scheduled_for", "platform", "created_by")
    search_fields = ("title", "team__name", "platform")
