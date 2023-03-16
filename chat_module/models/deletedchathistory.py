from ai_profiles.models import BotProfile
from allauth import app_settings
from django.db import models

from chat_module.models.validators import level_validation


class DeletedChatHistory(models.Model):
    """
    DeletedChatHistory Model
    ========================

    This model represents a deleted chat history between a user and a bot. Refer to ChatHistory.
    Note that this model does not require a 'user' and 'bot' pair to be unique, unlike ChatHistory.
    Therefore, interactions between a user and a bot can be deleted many times without causing a ValidationError.

    Attributes
    ----------
    user : ForeignKey
        The user involved in the chat.
    bot : ForeignKey
        The bot involved in the chat.
    history : JSONField
        The chat history.
    input_chars : IntegerField
        The number of input characters in the chat.
    level : DecimalField
        The level of the chat, represented as a decimal number. It is set to 1.0 by default.
    REQUIRED_FIELDS : List[str]
        A list of required fields, including "user", "bot", and "history".

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

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(DeletedChatHistory, self).save(*args, **kwargs)
