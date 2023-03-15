from ai_profiles.models import BotProfile
from allauth import app_settings
from django.db import models

from chat_module.models.validators import level_validation


class ChatHistory(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    bot = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    history = models.JSONField(blank=True)
    input_chars = models.IntegerField(default=0)
    level = models.DecimalField(
        max_digits=5, decimal_places=4, default=1.0, validators=[level_validation]
    )

    REQUIRED_FIELDS = ["user", "bot", "history"]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ChatHistory, self).save(*args, **kwargs)
