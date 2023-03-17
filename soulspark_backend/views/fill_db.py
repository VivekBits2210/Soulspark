import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import UserProfile


@api_view(["GET"])
def fill_db(request):
    image_path = os.path.join("static", "trial.jpg")
    with open(image_path, "rb") as f:
        image_content1 = f.read()

    image_path = os.path.join("static", "trial1.jpg")
    with open(image_path, "rb") as f:
        image_content2 = f.read()

    profile1_data = {
        "name": "Nicole",
        "gender": "F",
        "age": 18,
        "interests": "reading and running",
        "favorites": {"color": "red", "food": "pizza"},
        "physical_attributes": {"eyes": "blue"},
        "profession": "Air hostess",
        "profile_image": SimpleUploadedFile(
            "Nicole.jpg", image_content1, content_type="image/jpeg"
        ),
        "bio": "Lorem ipsum",
    }
    profile2_data = {
        "name": "Carla",
        "gender": "F",
        "age": 25,
        "interests": "hiking and jogging",
        "favorites": {"color": "blue", "food": "sushi"},
        "physical_attributes": {
            "eyes": "blue",
            "hair": "blonde",
            "skin": "fair",
            "figure": "slim",
        },
        "profession": "Secretary",
        "profile_image": SimpleUploadedFile(
            "Carla.jpg", image_content2, content_type="image/jpeg"
        ),
        "bio": "Lorem ipsum",
    }

    # Create the two BotProfile instances using the data
    BotProfile.objects.all().delete()
    UserProfile.objects.all().delete()
    profile1 = BotProfile(**profile1_data)
    profile2 = BotProfile(**profile2_data)

    # Save the profiles to the database
    profile1.save()
    profile2.save()
    return JsonResponse({"status": "ok"})
