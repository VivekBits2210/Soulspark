from ai_profiles.models import BotProfile
from allauth import app_settings
from django.db import models

from chat_module.models.validators import level_validation


class ChatHistory(models.Model):
    """
    .. default-role:: cmsreference

    ChatHistory Model
    =================

    This model represents the chat history between a user and a bot.

    Attributes
    ----------
    user : ForeignKey
        The user involved in the chat.
    bot : ForeignKey
        The bot involved in the chat.
    history : JSONField
        The chat history, as a list of JSON objects. Each object has a source, message and timestamp.
    input_chars : IntegerField
        The number of input characters from the user in the chat. This is useful for calculating level.
    level : DecimalField
        The level of progress the user has made with the bot, represented as a decimal number. It is set to 1.0 at the beginning.
    REQUIRED_FIELDS : List[str]
        A list of required fields, including "user", "bot", and "history".

    Meta
    ----
    unique_together : tuple
        Specifies that the combination of "user" and "bot" must be unique. Chat history is maintained per user, per bot, as one entry.

    Methods
    -------
    save(self, args, kwargs)
        Cleans the model instance and saves it to the database. Overridden to ensure that validators run.

    Notes
    -----
    This model requires the following imports:

    - ``from ai_profiles.models import BotProfile``
    - ``from allauth import app_settings``
    - ``from django.db import models``
    - ``from chat_module.models.validators import level_validation``
    """
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    bot = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    history = models.JSONField(blank=True)
    input_chars = models.IntegerField(default=0)
    level = models.DecimalField(
        max_digits=5, decimal_places=4, default=1.0, validators=[level_validation]
    )

    REQUIRED_FIELDS = ["user", "bot", "history"]

    class Meta:
        unique_together = ("user", "bot")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ChatHistory, self).save(*args, **kwargs)
