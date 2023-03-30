from django.core.files.uploadedfile import SimpleUploadedFile

from ai_profiles.models import BotProfile
from user_profiles.models import User, UserProfile
from user_profiles.utils import encrypt_email


def create_user_and_profile(
    email="email@email.com",
    first_name="Agent",
    last_name="Smith",
    age=25,
    gender="M",
    gender_focus="F",
    interests="java and python",
):
    user = User.objects.create(email=email, first_name=first_name, last_name=last_name)

    encrypted_email = encrypt_email(email).hex()

    profile = UserProfile.objects.create(
        user=user,
        age=age,
        gender=gender,
        gender_focus=gender_focus,
        interests=interests,
    )
    return user, encrypted_email, profile


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
