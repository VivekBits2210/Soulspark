import os

from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
import nltk

nltk.download("punkt")
from textblob import TextBlob


def plural_singular_detector(word):
    blob = TextBlob(word)
    singular = blob.words.singularize()[0]
    plural = blob.words.pluralize()[0]

    return singular, plural


def interests_validation(value):
    interests = value.split(",")
    for interest in interests:
        if not interest.strip():
            raise ValidationError("Invalid interests: comma-separated values expected.")


def validate_age(value):
    if value < 18 or value > 60:
        raise ValidationError("Age must be between 18 and 60.")


def validate_name(value):
    if not value.isalpha():
        raise ValidationError("Name must contain only alphabets.")
    if len(value.split()) > 1:
        raise ValidationError("Name must contain only one word.")


def validate_list(value):
    if not isinstance(value, list):
        raise ValidationError(
            "Expected a dictionary, but got %s" % type(value).__name__
        )


def validate_dict(value):
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
    interests : CharField
        The hobbies of the bot, represented as a string (e.g. "running and music").
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
    profession = models.CharField(max_length=100)
    interests = models.CharField(
        max_length=250, default="", blank=True, validators=[interests_validation]
    )
    favorites = models.JSONField(validators=[validate_dict], blank=True, default=dict)
    physical_attributes = models.JSONField(
        validators=[validate_dict], blank=True, default=dict
    )
    profile_image = models.ImageField(
        upload_to="images/", validators=[validate_image_extension]
    )
    searchable = models.BooleanField(default=True)
    summary = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.summary = self.generate_summary()
        return super(BotProfile, self).save(*args, **kwargs)

    def generate_summary(self):
        gender_string, pronoun, second_pronoun = self.get_gender_string()
        summary = f"{self.name} is a {self.age}-year-old {gender_string}. {pronoun} enjoys {self.interests}."
        summary += (
            f" {second_pronoun} {self.get_physical_attributes_string()}. {second_pronoun} favorite "
            f"{self.get_favorites_string()}."
        )

        return summary

    def get_physical_attributes_string(self):
        result = []
        if len(self.physical_attributes) == 0:
            return ""
        for key, value in self.physical_attributes.items():
            singular, plural = plural_singular_detector(key)
            string = f"{key} is {value}" if singular == key else f"{key} are {value}"
            result.append(string)
        return (
            ", ".join(result[:-1]) + " and " + result[-1]
            if len(result) > 1
            else result[0]
        )

    def get_favorites_string(self):
        result = []
        if len(self.favorites) == 0:
            return ""
        for key, value in self.favorites.items():
            string = f"{key} is {value}"
            result.append(string)
        return ", ".join(result[:-1]) + " and " + result[-1]

    def get_gender_string(self):
        if self.gender == "M":
            return tuple(["guy", "He", "His"])
        elif self.gender == "F":
            return tuple(["girl", "She", "Her"])
