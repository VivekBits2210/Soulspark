from django.db import models
from allauth import app_settings

from chat_module.models.validators import (
    gender_validation,
    gender_focus_validation,
    timezone_validation,
    experience_validation,
    interests_validation,
    age_validation,
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        app_settings.USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    age = models.PositiveIntegerField(
        null=True, blank=True, validators=[age_validation]
    )
    gender = models.CharField(
        max_length=10,
        choices=[("M", "Male"), ("F", "Female")],
        null=True,
        blank=True,
        validators=[gender_validation],
    )
    gender_focus = models.CharField(
        max_length=10,
        choices=[("M", "Male"), ("F", "Female"), ("E", "Everyone")],
        default="E",
        validators=[gender_focus_validation],
    )
    timezone = models.CharField(
        max_length=32, validators=[timezone_validation], default="America/New_York"
    )
    experience = models.PositiveIntegerField(
        default=1, validators=[experience_validation]
    )
    interests = models.CharField(
        max_length=250, default="", blank=True, validators=[interests_validation]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(UserProfile, self).save(*args, **kwargs)
