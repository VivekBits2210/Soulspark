from rest_framework import serializers
from .models import BotProfile

class BotProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotProfile
        exclude = ['bot_id']