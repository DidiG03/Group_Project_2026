from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from messaging_app.models import Message
from organization.models import Department
from scheduling.models import Meeting
from teams.models import Team, TeamDependency, TeamMember, TeamStatusHistory

from .current_user import get_current_user
from .models import AuditLog, Notification


def _create_audit_log(instance, action):
    AuditLog.objects.create(
        actor=get_current_user(),
        action=action,
        model_name=instance.__class__.__name__,
        object_pk=str(instance.pk),
        object_label=str(instance),
    )


@receiver(post_save, sender=Department)
@receiver(post_save, sender=Team)
@receiver(post_save, sender=TeamMember)
@receiver(post_save, sender=TeamDependency)
@receiver(post_save, sender=Message)
@receiver(post_save, sender=Meeting)
def on_save(sender, instance, created, **kwargs):
    _create_audit_log(instance, "created" if created else "updated")


@receiver(post_save, sender=TeamStatusHistory)
def on_team_status_change(sender, instance, created, **kwargs):
    if not created:
        return
    manager = instance.team.manager
    if manager:
        Notification.objects.create(
            user=manager,
            title=f"{instance.team.name} status updated",
            body=f"Changed from {instance.old_status} to {instance.new_status}.",
        )


@receiver(post_delete, sender=Department)
@receiver(post_delete, sender=Team)
@receiver(post_delete, sender=TeamMember)
@receiver(post_delete, sender=TeamDependency)
@receiver(post_delete, sender=Message)
@receiver(post_delete, sender=Meeting)
def on_delete(sender, instance, **kwargs):
    _create_audit_log(instance, "deleted")
