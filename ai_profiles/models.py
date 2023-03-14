import os

from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError


def validate_age(value):
    if value < 18 or value > 60:
        raise ValidationError('Age must be between 18 and 60.')


def validate_name(value):
    if not value.isalpha():
        raise ValidationError('Name must contain only alphabets.')
    if len(value.split()) > 1:
        raise ValidationError('Name must contain only one word.')


def validate_json(value):
    if not isinstance(value, dict):
        raise ValidationError("Expected a dictionary, but got %s" % type(value).__name__)


def validate_image_extension(value):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # add any other allowed file extensions here
    ext = os.path.splitext(value.name)[-1]
    if not ext.lower() in allowed_extensions:
        raise ValidationError(
            'Only image files with the following extensions are allowed: %s' % ', '.join(allowed_extensions))


class BotProfile(models.Model):
    bot_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, validators=[validate_name])
    gender = models.CharField(max_length=1,
                              validators=[RegexValidator(regex='^[MF]$', message='Gender must be either M or F')])
    age = models.IntegerField(validators=[validate_age])
    bio = models.CharField(max_length=300)
    profession = models.TextField()
    hobbies = models.JSONField(validators=[validate_json])
    favorites = models.JSONField(validators=[validate_json])
    physical_attributes = models.JSONField(validators=[validate_json])
    profile_image = models.ImageField(upload_to='images/', validators=[validate_image_extension])

    def get_id(self):
        return self.bot_id

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BotProfile, self).save(*args, **kwargs)
