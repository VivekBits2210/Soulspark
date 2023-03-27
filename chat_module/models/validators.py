from django.core.exceptions import ValidationError


def level_validation(value):
    if value < 1.0:
        raise ValidationError(f"{value} is not a valid level, should be >= 1.0.")
