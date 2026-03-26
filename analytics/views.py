from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView

from organization.models import Department
from teams.models import Team


class ChartsView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/charts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        department_rows = Department.objects.annotate(team_total=Count("teams")).values("name", "team_total")
        manager_rows = (
            Team.objects.exclude(manager__isnull=True)
            .values("manager__first_name", "manager__last_name")
            .annotate(team_total=Count("id"))
        )

        context["department_labels"] = [row["name"] for row in department_rows]
        context["department_values"] = [row["team_total"] for row in department_rows]
        context["manager_labels"] = [
            f'{row["manager__first_name"]} {row["manager__last_name"]}' for row in manager_rows
        ]
        context["manager_values"] = [row["team_total"] for row in manager_rows]
        return context
