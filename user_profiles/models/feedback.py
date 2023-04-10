from django.db import models
from user_profiles.models.user import User


class UserFeedback(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=None
    )
    feedback = models.TextField()
