from django.db import models


class TelegramUser(models.Model):
    """Model to store telegram user data"""

    username = models.CharField(max_length=100, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username or self.first_name
