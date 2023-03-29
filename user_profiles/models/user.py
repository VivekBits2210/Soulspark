from django.db import models
from django.core.validators import validate_email


class User(models.Model):
    email = models.EmailField(primary_key=True, unique=True, validators=[validate_email])
    first_name = models.TextField(default="")
    last_name = models.TextField(default="")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(User, self).save(*args, **kwargs)