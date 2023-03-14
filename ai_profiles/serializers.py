from rest_framework import serializers
from .models import BotProfile


# class BotProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BotProfile
#         fields = ['name', 'gender', 'age', 'bio', 'profession', 'hobbies', 'favorites', 'profile_image']

class BotProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotProfile
        exclude = ['bot_id']