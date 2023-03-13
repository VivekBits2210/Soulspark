from django.db import models

# Create your models here.
from allauth import app_settings
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(app_settings.USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True)
    gender_focus = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True)
    level = models.CharField(max_length=50, default=1)
    interests = models.CharField(max_length=250, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']
