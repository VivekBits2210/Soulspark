import pytz
from django.core.exceptions import ValidationError
from ai_profiles.models import BotProfile
from allauth import app_settings
from django.db import models


def timezone_validation(value):
    try:
        pytz.timezone(value)
    except pytz.UnknownTimeZoneError:
        raise ValidationError(f"{value} is not a valid timezone.")


def gender_validation(value):
    if value not in ['M', 'F']:
        raise ValidationError(f"{value} is not a valid gender.")


def level_validation(value):
    if value < 1.0:
        raise ValidationError(f"{value} is not a valid level, should be >= 1.0.")


def interests_validation(value):
    interests = value.split(',')
    for interest in interests:
        if not interest.strip():
            raise ValidationError("Invalid interests: comma-separated values expected.")


def age_validation(value):
    if value < 13:
        raise ValidationError("Age must be 13 or older.")


class UserProfile(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[age_validation])
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True,
                              blank=True, validators=[gender_validation])
    gender_focus = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True,
                                    blank=True, validators=[gender_validation])
    timezone = models.CharField(max_length=32, validators=[timezone_validation], default='America/New_York')
    experience = models.IntegerField(default=0)
    interests = models.CharField(max_length=250, null=True, blank=True, validators=[interests_validation])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(UserProfile, self).save(*args, **kwargs)


class ChatHistory(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    bot = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    history = models.JSONField(blank=True)
    input_chars = models.IntegerField(default=0)
    level = models.DecimalField(max_digits=5, decimal_places=4, default=1.0, validators=[level_validation])

    REQUIRED_FIELDS = ['user', 'bot', 'history']

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ChatHistory, self).save(*args, **kwargs)


class DeletedChatHistory(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    bot = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    history = models.JSONField()
    input_chars = models.IntegerField(default=0)
    level = models.DecimalField(max_digits=5, decimal_places=4, default=1.0)

    REQUIRED_FIELDS = ['user', 'bot', 'history']

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(DeletedChatHistory, self).save(*args, **kwargs)
