from django.urls import path

from .views import ReportsHomeView, TeamSummaryCsvView, TeamSummaryPdfView

urlpatterns = [
    path("", ReportsHomeView.as_view(), name="reports_home"),
    path("summary/csv/", TeamSummaryCsvView.as_view(), name="report_csv"),
    path("summary/pdf/", TeamSummaryPdfView.as_view(), name="report_pdf"),
]
