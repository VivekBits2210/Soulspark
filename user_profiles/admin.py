from django.contrib import admin
from user_profiles.models import User, UserProfile, UserFeedback

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserFeedback)
# Register your models here.
