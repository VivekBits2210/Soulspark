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
    """
UserProfile Model
==================

This model represents a user profile.

Attributes
----------
user : OneToOneField
    The user associated with the profile.
age : PositiveIntegerField
    The age of the user.
gender : CharField
    The gender of the user, represented as "M" (male) or "F" (female).
gender_focus : CharField
    The gender focus of the user, represented as "M" (male), "F" (female), or "E" (everyone). The default value is "E".
timezone : CharField
    The timezone of the user.
experience : PositiveIntegerField
    The experience points of the user.
interests : CharField
    The interests of the user, separated by commas.
is_active : BooleanField
    Indicates whether the user is active.
is_staff : BooleanField
    Indicates whether the user is staff.

Methods
-------
save(self, args, kwargs)
    Cleans the model instance and saves it to the database. Custom save functions runs validators before saving any model object

Notes
-----
This model requires the following imports:

- ``from django.db import models``
- ``from allauth import app_settings``
- ``from chat_module.models.validators``

This model uses the following validators:

- ``age_validation``: Validates that the user is 13 years old or older.
- ``gender_validation``: Validates that the gender is "M" (male) or "F" (female).
- ``gender_focus_validation``: Validates that the gender focus is "M" (male), "F" (female), or "E" (everyone).
- ``timezone_validation``: Validates that the timezone is a valid timezone.
- ``experience_validation``: Validates that the experience points are greater than or equal to 0.
- ``interests_validation``: Validates that the interests are valid comma-separated values.
    """
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
