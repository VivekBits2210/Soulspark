from django.db import models


class GPTUsageRecord(models.Model):
    email = models.CharField(max_length=200, default="email@email.com")
    bot_name = models.CharField(max_length=50, default="default_bot_name")
    indicator_tokens = models.IntegerField(default=0)
    story_tokens = models.IntegerField(default=0)
    summarizer_tokens = models.IntegerField(default=0)
    indicator_vector = models.CharField(max_length=100)
    indicator_version = models.CharField(max_length=10)
    chat_history_length = models.IntegerField(default=0)

    REQUIRED_FIELDS = [
        "email",
        "bot_name",
        "indicator_tokens",
        "story_tokens",
        "indicator_vector",
        "indicator_version",
        "chat_history_length",
    ]

    def __str__(self):
        return (
            f"GPTUsageRecord({self.email}, {self.bot_name}, indicator_tokens={self.indicator_tokens}, "
            f"story_tokens={self.story_tokens}, summarizer_tokens={self.summarizer_tokens}, "
            f"indicator_vector={self.indicator_vector}, indicator_version={self.indicator_version}, "
            f"chat_history_length={self.chat_history_length})"
        )
