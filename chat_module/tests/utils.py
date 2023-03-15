import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from ai_profiles.models import BotProfile
from chat_module.models import UserProfile


def create_user(
    username="testuser",
    password="testpass",
    age=25,
    gender="M",
    gender_focus="F",
    interests="test,python",
):
    user = User.objects.create(username=username, password=password)
    UserProfile.objects.create(
        user=user,
        age=age,
        gender=gender,
        gender_focus=gender_focus,
        interests=interests,
    )
    return user


def create_bot():
    image_path = os.path.join("static", "trial.jpg")
    with open(image_path, "rb") as f:
        image_content = f.read()

    valid_data = {
        "name": "Jane",
        "gender": "F",
        "age": 30,
        "bio": "I am a chatbot too.",
        "profession": "Engineer",
        "hobbies": {"reading": "novels", "sport": "cricket"},
        "physical_attributes": {"hair": "black"},
        "favorites": {"color": "blue", "food": "pizza"},
        "profile_image": SimpleUploadedFile(
            "test_serializer.jpg", image_content, content_type="image/jpeg"
        ),
    }
    bot_profile = BotProfile.objects.create(**valid_data)
    return bot_profile
