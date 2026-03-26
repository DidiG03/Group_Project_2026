from django.contrib import admin

from .models import Team, TeamDependency, TeamMember, TeamStatusHistory


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "manager", "status", "updated_at")
    search_fields = ("name", "department__name", "manager__username")
    list_filter = ("department", "status")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "team", "role", "email")
    search_fields = ("full_name", "email", "team__name")


@admin.register(TeamDependency)
class TeamDependencyAdmin(admin.ModelAdmin):
    list_display = ("from_team", "to_team", "relation_type")
    list_filter = ("relation_type",)


@admin.register(TeamStatusHistory)
class TeamStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("team", "old_status", "new_status", "changed_at")
    search_fields = ("team__name",)
