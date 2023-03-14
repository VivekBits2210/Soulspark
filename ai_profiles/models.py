import os

from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError


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
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, validators=[RegexValidator(regex='^[MF]$', message='Gender must be either M or F')])
    age = models.IntegerField()
    bio = models.CharField(max_length=300)
    profession = models.TextField()
    hobbies = models.JSONField(validators=[validate_json])
    favorites = models.JSONField(validators=[validate_json])
    profile_image = models.ImageField(upload_to='images/', validators=[validate_image_extension])

    def get_id(self):
        return self.bot_id

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BotProfile, self).save(*args, **kwargs)
