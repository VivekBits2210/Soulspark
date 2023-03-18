from ai_profiles.models import BotProfile
from allauth import app_settings
from django.db import models


class GPTUsageRecord(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    bot = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    indicator_tokens = models.IntegerField(default=0)
    story_tokens = models.IntegerField(default=0)
    summarizer_tokens = models.IntegerField(default=0)
    indicator_vector = models.CharField(max_length=100)
    indicator_version = models.CharField(max_length=10)
    chat_history_length = models.IntegerField(default=0)

    REQUIRED_FIELDS = [
        "user",
        "bot",
        "indicator_tokens",
        "story_tokens",
        "indicator_vector",
        "indicator_version",
        "chat_history_length",
    ]

    class Meta:
        unique_together = ("user", "bot", "chat_history_length")

    def __str__(self):
        return f"GPTUsageRecord({self.user.username}, {self.bot.name}, indicator_tokens={self.indicator_tokens}, " \
               f"story_tokens={self.story_tokens}, summarizer_tokens={self.summarizer_tokens}, " \
               f"indicator_vector={self.indicator_vector}, indicator_version={self.indicator_version}, " \
               f"chat_history_length={self.chat_history_length})"
