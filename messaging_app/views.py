from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView

from core.models import Notification
from teams.models import Team

from .forms import MessageForm
from .models import Message


class InboxView(LoginRequiredMixin, ListView):
    template_name = "messaging_app/inbox.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(recipients=self.request.user, status=Message.Status.SENT).select_related("sender")


class SentView(LoginRequiredMixin, ListView):
    template_name = "messaging_app/sent.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user, status=Message.Status.SENT)


class DraftView(LoginRequiredMixin, ListView):
    template_name = "messaging_app/draft.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user, status=Message.Status.DRAFT)


class MessageCreateView(LoginRequiredMixin, CreateView):
    form_class = MessageForm
    template_name = "messaging_app/message_form.html"
    success_url = "/messages/inbox/"

    def get_initial(self):
        initial = super().get_initial()
        team_id = self.request.GET.get("team")
        if team_id:
            team = get_object_or_404(Team, pk=team_id)
            initial["subject"] = f"Update for {team.name}"
            member_lines = "\n".join(
                f"- {m.full_name} <{m.email}>" for m in team.members.all()
            )
            initial["body"] = (
                f"Hello {team.name} team,\n\n"
                "Sharing an update here.\n\n"
                + (f"Team members on copy:\n{member_lines}\n\n" if member_lines else "")
                + "Thanks."
            )
            if team.manager:
                initial["recipients"] = [team.manager.pk]
        return initial

    def form_valid(self, form):
        form.instance.sender = self.request.user
        if form.instance.status == Message.Status.SENT:
            form.instance.sent_at = timezone.now()
        response = super().form_valid(form)
        if self.object.status == Message.Status.SENT:
            for recipient in self.object.recipients.all():
                Notification.objects.create(
                    user=recipient,
                    title=f"New message: {self.object.subject}",
                    body=f"From {self.request.user.username}",
                )
        return response


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "shared/confirm_delete.html"
    success_url = "/messages/inbox/"

    def get_queryset(self):
        return Message.objects.filter(Q(sender=self.request.user) | Q(recipients=self.request.user)).distinct()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Message deleted.")
        return redirect(self.success_url)
