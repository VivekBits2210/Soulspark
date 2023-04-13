from ai_profiles.models import BotProfile
from django.db import models

from chat_module.models.validators import level_validation
from user_profiles.models import User


class DeletedChatHistory(models.Model):
    email = models.CharField(max_length=200, default="email@email.com")
    bot_name = models.CharField(max_length=50, default="default_bot_name")
    history = models.JSONField(blank=True)
    input_chars = models.IntegerField(default=0)
    level = models.DecimalField(
        max_digits=5, decimal_places=4, default=1.0, validators=[level_validation]
    )

    REQUIRED_FIELDS = ["user", "bot", "history"]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(DeletedChatHistory, self).save(*args, **kwargs)
