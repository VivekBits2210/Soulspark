from ai_profiles.models import BotProfile
from django.db import models

from chat_module.models.validators import level_validation
from user_profiles.models import User


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    history = models.JSONField(blank=True, default=list)
    input_chars = models.IntegerField(default=0)
    level = models.DecimalField(
        max_digits=5, decimal_places=4, default=1.0, validators=[level_validation]
    )
    user_summary = models.JSONField(blank=True, default=list)
    bot_summary = models.JSONField(blank=True, default=list)
    summary_index = models.IntegerField(default=-1, null=True)

    REQUIRED_FIELDS = ["user", "bot", "history"]

    class Meta:
        unique_together = ("user", "bot")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ChatHistory, self).save(*args, **kwargs)
