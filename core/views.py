from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.db.models import Q
from django.views.generic import ListView, TemplateView, View

from organization.models import Department
from teams.models import Team

from .models import AuditLog, Notification


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        display_mode = self.request.GET.get("view", "grid")

        teams = Team.objects.select_related("department", "manager")
        departments = Department.objects.all()
        managers = (
            Team.objects.exclude(manager__isnull=True)
            .values_list("manager__first_name", "manager__last_name", "manager__email")
            .distinct()
        )

        if query:
            teams = teams.filter(
                Q(name__icontains=query)
                | Q(mission__icontains=query)
                | Q(manager__first_name__icontains=query)
                | Q(manager__last_name__icontains=query)
                | Q(department__name__icontains=query)
            )
            departments = departments.filter(
                Q(name__icontains=query) | Q(leader_name__icontains=query)
            )
            managers = (
                Team.objects.filter(Q(manager__first_name__icontains=query) | Q(manager__last_name__icontains=query))
                .exclude(manager__isnull=True)
                .values_list("manager__first_name", "manager__last_name", "manager__email")
                .distinct()
            )

        all_departments = Department.objects.prefetch_related("teams").all()
        low_engineer_teams = [
            team for team in Team.objects.filter(status=Team.TeamStatus.ACTIVE) if team.engineer_count < 5
        ]
        low_team_departments = [department for department in all_departments if department.teams.count() < 3]

        compliance_notes = []
        if Department.objects.count() < 2:
            compliance_notes.append("At least two departments are required by the brief.")
        if low_team_departments:
            compliance_notes.append(
                f"{len(low_team_departments)} department(s) currently have fewer than 3 teams."
            )
        if low_engineer_teams:
            compliance_notes.append(
                f"{len(low_engineer_teams)} active team(s) currently have fewer than 5 engineers."
            )

        context["query"] = query
        context["display_mode"] = "list" if display_mode == "list" else "grid"
        context["teams"] = teams[:10]
        context["departments"] = departments[:10]
        context["managers"] = managers[:10]
        context["team_count"] = Team.objects.count()
        context["active_team_count"] = Team.objects.filter(status=Team.TeamStatus.ACTIVE).count()
        context["department_count"] = Department.objects.count()
        context["compliance_notes"] = compliance_notes
        context["unread_notifications_count"] = Notification.objects.filter(
            user=self.request.user, is_read=False
        ).count()
        return context


class NotificationListView(LoginRequiredMixin, ListView):
    template_name = "core/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        Notification.objects.filter(pk=pk, user=request.user).update(is_read=True)
        return redirect("notifications")


class AuditLogListView(LoginRequiredMixin, ListView):
    template_name = "core/audit_log.html"
    context_object_name = "audit_logs"
    paginate_by = 50

    def get_queryset(self):
        return AuditLog.objects.select_related("actor").all()


def custom_page_not_found(request, exception=None):
    return render(request, "404.html", status=404)
