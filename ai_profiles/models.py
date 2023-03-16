import os

from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError


def validate_age(value):
    if value < 18 or value > 60:
        raise ValidationError("Age must be between 18 and 60.")


def validate_name(value):
    if not value.isalpha():
        raise ValidationError("Name must contain only alphabets.")
    if len(value.split()) > 1:
        raise ValidationError("Name must contain only one word.")


def validate_json(value):
    if not isinstance(value, dict):
        raise ValidationError(
            "Expected a dictionary, but got %s" % type(value).__name__
        )


def validate_image_extension(value):
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    ext = os.path.splitext(value.name)[-1]
    if not ext.lower() in allowed_extensions:
        raise ValidationError(
            "Only image files with the following extensions are allowed: %s"
            % ", ".join(allowed_extensions)
        )


class BotProfile(models.Model):
    """
BotProfile Model
=================

This model represents a bot profile.

Attributes
----------
bot_id : AutoField
    The ID of the bot.
name : CharField
    The name of the bot.
gender : CharField
    The gender of the bot, represented as "M" (male) or "F" (female).
age : IntegerField
    The age of the bot.
bio : CharField
    The biography of the bot.
profession : TextField
    The profession of the bot.
hobbies : JSONField
    The hobbies of the bot, represented as a dictionary.
favorites : JSONField
    The favorites of the bot, represented as a dictionary.
physical_attributes : JSONField
    The physical attributes of the bot, represented as a dictionary.
profile_image : ImageField
    The profile image of the bot.
searchable : BooleanField
    Indicates whether the bot is searchable. Customized bot profiles are not searchable as they are specific to a user.
    The fetch_profile endpoint can only fetch searchable profiles. In order to fetch customized bot profile, use fetch_chat_history
    without the bot_id parameter.

Methods
-------
save(self, args, kwargs)
    Cleans the model instance and saves it to the database. This function runs validators before saving any data to the database.

Notes
-----
This model requires the following imports:

- ``from os import path``
- ``from django.core.validators import RegexValidator``
- ``from django.db import models``
- ``from django.core.exceptions import ValidationError``

This model uses the following validators:

- ``validate_age``: Validates that the age is between 18 and 60.
- ``validate_name``: Validates that the name contains only alphabets and only one word.
- ``validate_json``: Validates that the value is a dictionary.
- ``validate_image_extension``: Validates that the image has a valid extension (.jpg, .jpeg, or .png).
    """
    bot_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, validators=[validate_name])
    gender = models.CharField(
        max_length=1,
        validators=[
            RegexValidator(regex="^[MF]$", message="Gender must be either M or F")
        ],
    )
    age = models.IntegerField(validators=[validate_age])
    bio = models.CharField(max_length=300)
    profession = models.TextField()
    hobbies = models.JSONField(validators=[validate_json])
    favorites = models.JSONField(validators=[validate_json])
    physical_attributes = models.JSONField(validators=[validate_json])
    profile_image = models.ImageField(
        upload_to="images/", validators=[validate_image_extension]
    )
    searchable = models.BooleanField(default=True)
    summary = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        self.summary = self.generate_summary()
        self.full_clean()
        return super(BotProfile, self).save(*args, **kwargs)

    # TODO: clean up the summary (favorites etc)
    def generate_summary(self):
        summary = ""
        # gender = "Male" if self.gender == "M" else "Female"
        # hobbies = ", ".join(self.hobbies.values())
        # favorites = ", ".join(self.favorites.values())
        # physical_attributes = ", ".join(
        #     [f"{key}: {value}" for key, value in self.physical_attributes.items()]
        # )
        #
        # summary = f"{self.name} is a {gender} {self.age}-year-old {self.profession}. "
        # summary += f"{self.name}'s hobbies include {hobbies}. "
        # summary += f"{self.name}'s favorite things are {favorites}. "
        # summary += f"{self.name} has {physical_attributes}."

        return summary
