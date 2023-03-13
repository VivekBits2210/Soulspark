from rest_framework import serializers
from .models import BotProfile

class BotProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotProfile
        fields = ['bot_id', 'gender', 'age', 'profession', 'hobbies', 'favorites', 'profile_image']