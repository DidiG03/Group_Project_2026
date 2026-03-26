from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import TeamDependencyForm, TeamForm, TeamMemberForm
from .models import Team, TeamDependency, TeamMember


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "teams/team_list.html"
    context_object_name = "teams"

    def get_queryset(self):
        queryset = Team.objects.select_related("department", "manager")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(department__name__icontains=query)
                | Q(manager__first_name__icontains=query)
                | Q(manager__last_name__icontains=query)
            )
        return queryset


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "teams/team_detail.html"
    context_object_name = "team"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context["members"] = team.members.all()
        context["dependencies_from"] = team.dependencies_from.select_related("to_team")
        context["dependencies_to"] = team.dependencies_to.select_related("from_team")
        return context


class TeamCreateView(LoginRequiredMixin, CreateView):
    form_class = TeamForm
    template_name = "teams/team_form.html"
    success_url = reverse_lazy("team_list")


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "teams/team_form.html"
    success_url = reverse_lazy("team_list")


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("team_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Team deleted.")
            return redirect(self.success_url)
        except ValidationError as exc:
            messages.error(request, str(exc))
            return self.get(request, *args, **kwargs)


class TeamMemberCreateView(LoginRequiredMixin, CreateView):
    form_class = TeamMemberForm
    template_name = "teams/team_member_form.html"
    success_url = reverse_lazy("team_list")


class TeamMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = TeamMember
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("team_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Team member deleted.")
            return redirect(self.success_url)
        except ValidationError as exc:
            messages.error(request, str(exc))
            return self.get(request, *args, **kwargs)


class TeamDependencyCreateView(LoginRequiredMixin, CreateView):
    form_class = TeamDependencyForm
    template_name = "teams/team_dependency_form.html"
    success_url = reverse_lazy("team_list")
