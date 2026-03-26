from django.contrib import admin

from .models import Department, TeamType


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "leader_name", "specialisation", "is_active")
    search_fields = ("name", "leader_name", "specialisation")
    list_filter = ("is_active",)


@admin.register(TeamType)
class TeamTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
