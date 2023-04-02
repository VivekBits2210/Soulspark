from django.db import models

from user_profiles.models.user import User
from user_profiles.models.validators import (
    gender_validation,
    gender_focus_validation,
    timezone_validation,
    experience_validation,
    interests_validation,
    age_validation,
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=None
    )
    name = models.TextField(blank=True, default="")
    age = models.PositiveIntegerField(
        null=True, blank=True, validators=[age_validation]
    )
    gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female")],
        null=True,
        blank=True,
        validators=[gender_validation],
    )
    gender_focus = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female"), ("E", "Everyone")],
        default="E",
        validators=[gender_focus_validation],
    )
    country = models.TextField(null=True, default="USA")
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
    summary = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.name = self.user.first_name
        self.summary = self.generate_summary()
        return super(UserProfile, self).save(*args, **kwargs)

    def generate_summary(self):
        gender_string, pronoun = self.get_gender_string()
        gender_focus_string = self.get_gender_focus_string()

        summary = (
            f"{self.name} is a {self.age}-year-old" if self.age else f"{self.name} is a"
        )
        summary += f" {gender_string}" if gender_string else ""
        summary += (
            f" interested in {gender_focus_string}" if gender_focus_string else ""
        )
        summary += (
            f". {pronoun} lives in the country {self.country}" if self.country else ""
        )
        summary += (
            f". {pronoun} enjoys {self.interests}." if self.interests != "" else "."
        )
        return summary

    def get_gender_string(self):
        if self.gender == "M":
            return tuple(["guy", "He"])
        elif self.gender == "F":
            return tuple(["girl", "She"])
        elif not self.gender:
            return tuple([None, "They"])

    def get_gender_focus_string(self):
        if self.gender_focus == "M":
            return "men"
        elif self.gender_focus == "F":
            return "women"
        elif self.gender_focus == "E":
            return "both men and women"
        elif not self.gender_focus:
            return None
