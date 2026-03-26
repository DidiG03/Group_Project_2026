from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "status", "created_at", "sent_at")
    search_fields = ("subject", "sender__username")
    list_filter = ("status",)
