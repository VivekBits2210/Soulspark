import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from ai_profiles.models import BotProfile
from chat_module.models import UserProfile


def create_user_and_profile(
        username="tester",
        password="testpassword",
        first_name="Name",
        age=25,
        gender="M",
        gender_focus="F",
        interests="java and python",
):
    user = get_user_model().objects.create_user(username=username, first_name=first_name, password=password)
    profile = UserProfile.objects.create(
        user=user,
        age=age,
        gender=gender,
        gender_focus=gender_focus,
        interests=interests,
    )
    return user, profile


def create_bot(name="John"):
    bot = BotProfile.objects.create(
        name=name,
        gender="F",
        age=25,
        bio="I am a chatbot.",
        profession="AI assistant",
        interests="jogging and music",
        favorites={"color": "blue", "food": "pizza"},
        physical_attributes={"hair": "black"},
        profile_image=SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        ),
    )
    return bot
