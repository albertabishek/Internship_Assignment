from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_mock_email_task


@receiver(post_save, sender=User)
def send_welcome_email_on_creation(sender, instance, created, **kwargs):
    """
    When a new user is created, trigger the background task to send an email.
    """
    if created:
        print(
            f"Signal received! New user '{instance.username}' created. Trigger email task."
        )
        send_mock_email_task.delay(instance.email)
