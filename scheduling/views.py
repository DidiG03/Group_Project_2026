from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.models import Notification
from teams.models import Team

from .forms import MeetingForm
from .models import Meeting


class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = "scheduling/meeting_list.html"
    context_object_name = "meetings"

    def get_queryset(self):
        return Meeting.objects.select_related("team").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["upcoming"] = Meeting.objects.filter(scheduled_for__gte=now).order_by("scheduled_for")[:10]
        context["weekly"] = Meeting.objects.filter(
            scheduled_for__gte=now, scheduled_for__lt=now + timedelta(days=7)
        )
        context["monthly"] = Meeting.objects.filter(
            scheduled_for__gte=now, scheduled_for__lt=now + timedelta(days=30)
        )
        return context


class MeetingCreateView(LoginRequiredMixin, CreateView):
    form_class = MeetingForm
    template_name = "scheduling/meeting_form.html"
    success_url = "/schedule/"

    def get_initial(self):
        initial = super().get_initial()
        team_id = self.request.GET.get("team")
        if team_id:
            team = get_object_or_404(Team, pk=team_id)
            initial["team"] = team
            initial["title"] = f"{team.name} sync"
            initial["platform"] = "Microsoft Teams"
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        manager = self.object.team.manager
        if manager and manager != self.request.user:
            Notification.objects.create(
                user=manager,
                title=f"Meeting scheduled for {self.object.team.name}",
                body=f"{self.object.title} at {self.object.scheduled_for}",
            )
        return response


class MeetingUpdateView(LoginRequiredMixin, UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = "scheduling/meeting_form.html"
    success_url = "/schedule/"


class MeetingDeleteView(LoginRequiredMixin, DeleteView):
    model = Meeting
    template_name = "shared/confirm_delete.html"
    success_url = "/schedule/"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Meeting deleted.")
        return redirect(self.success_url)
