from ai_profiles.models import BotProfile
from allauth import app_settings
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True)
    gender_focus = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True)
    experience = models.IntegerField(default=0)
    interests = models.CharField(max_length=250, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']


class ChatHistory(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    bot = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    history = models.JSONField()
    input_chars = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    progress = models.FloatField(default=0.0)

    REQUIRED_FIELDS = ['user', 'bot', 'history']


class DeletedChatHistory(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    bot = models.ForeignKey(BotProfile, on_delete=models.CASCADE)
    history = models.JSONField()

    REQUIRED_FIELDS = ['user', 'bot', 'history']
