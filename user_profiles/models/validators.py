import pytz
from django.core.exceptions import ValidationError


def timezone_validation(value):
    try:
        pytz.timezone(value)
    except pytz.UnknownTimeZoneError:
        raise ValidationError(f"{value} is not a valid timezone.")


def gender_validation(value):
    if value not in ["M", "F"]:
        raise ValidationError(f"{value} is not a valid gender.")


def gender_focus_validation(value):
    if value not in ["M", "F", "E"]:
        raise ValidationError(f"{value} is not a valid gender focus.")


def experience_validation(value):
    if value < 0:
        raise ValidationError(
            f"{value} is not a valid experience points value, should be >=0."
        )


def interests_validation(value):
    interests = value.split(",")
    for interest in interests:
        if not interest.strip():
            raise ValidationError("Invalid interests: comma-separated values expected.")


def age_validation(value):
    if value < 13:
        raise ValidationError("Age must be 13 or older.")
