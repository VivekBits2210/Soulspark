from django.db import models

# Create your models here.
from django.db import models


class UserProfile(models.Model):
    UID = models.CharField(max_length=100, primary_key=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    level = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['age', 'gender', 'level']
