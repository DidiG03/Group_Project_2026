from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from teams.models import TeamDependency

from .forms import DepartmentForm, TeamTypeForm
from .models import Department, TeamType


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = "organization/department_list.html"
    context_object_name = "departments"


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    form_class = DepartmentForm
    template_name = "organization/department_form.html"
    success_url = reverse_lazy("department_list")


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "organization/department_form.html"
    success_url = reverse_lazy("department_list")


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("department_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Department deleted.")
            return redirect(self.success_url)
        except ValidationError as exc:
            messages.error(request, str(exc))
            return self.get(request, *args, **kwargs)


class TeamTypeCreateView(LoginRequiredMixin, CreateView):
    form_class = TeamTypeForm
    template_name = "organization/teamtype_form.html"
    success_url = reverse_lazy("department_list")


class OrganizationStructureView(LoginRequiredMixin, TemplateView):
    template_name = "organization/structure.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.prefetch_related("teams").all()
        context["dependencies"] = TeamDependency.objects.select_related("from_team", "to_team")
        context["team_types"] = TeamType.objects.all()
        return context
