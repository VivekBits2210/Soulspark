from rest_framework import serializers
from ai_profiles.models import BotProfile


class BotProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotProfile
        exclude = ["bot_id"]
