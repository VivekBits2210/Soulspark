from rest_framework import serializers
from ai_profiles.models import BotProfile


class BotProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotProfile
        exclude = [
            "bot_profile_id",
            "summary",
        ]  # TODO: Check why summary missing wasn't being detected by a serializer test
