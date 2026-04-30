import csv
from io import BytesIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from teams.models import Team


class ReportsHomeView(LoginRequiredMixin, TemplateView):
    template_name = "reports/reports_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = Team.objects.select_related("department", "manager").all()
        teams_without_manager = teams.filter(manager__isnull=True)
        context["team_count"] = teams.count()
        context["teams_without_manager"] = teams_without_manager
        context["summary_rows"] = teams
        return context


class TeamSummaryCsvView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="team_summary.csv"'

        writer = csv.writer(response)
        writer.writerow(["Team", "Department", "Manager", "Engineers", "Status", "Contact"])

        for team in Team.objects.select_related("department", "manager").all():
            writer.writerow(
                [
                    team.name,
                    team.department.name,
                    team.manager.get_full_name() if team.manager else "",
                    team.engineer_count,
                    team.get_status_display(),
                    team.contact_channel,
                ]
            )
        return response


class TeamSummaryPdfView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 40
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, y, "Engineering Team Summary Report")
        y -= 25
        pdf.setFont("Helvetica", 10)

        for team in Team.objects.select_related("department", "manager").all():
            line = (
                f"{team.name} | Dept: {team.department.name} | "
                f"Manager: {team.manager.get_full_name() if team.manager else 'N/A'} | "
                f"Engineers: {team.engineer_count}"
            )
            pdf.drawString(40, y, line[:120])
            y -= 16
            if y < 60:
                pdf.showPage()
                y = height - 40
                pdf.setFont("Helvetica", 10)

        pdf.save()
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="team_summary.pdf"'
        return response
