import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from user_profiles.models import UserProfile


@api_view(["GET"])
def fill_db(request):
    image_content = []
    for file in ["trial","trial1","Nicole","Sheanguang"]:
        image_path = os.path.join("static", f"{file}.jpg")
        with open(image_path, "rb") as f:
            image_content.append(f.read())

    profile1_data = {
        "name": "Nicole",
        "gender": "F",
        "age": 18,
        "interests": "reading and running",
        "favorites": {"color": "red", "food": "pizza"},
        "physical_attributes": {"eyes": "blue"},
        "profession": "Air hostess",
        "profile_image": SimpleUploadedFile(
            "Nicole.jpg", image_content[0], content_type="image/jpeg"
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
            "Carla.jpg", image_content[1], content_type="image/jpeg"
        ),
        "bio": "Lorem ipsum",
    }
    profile3_data = {
        "name": "Aurelia",
        "gender": "F",
        "age": 19,
        "interests": "hiking and jogging",
        "favorites": {"color": "blue", "food": "sushi"},
        "physical_attributes": {
            "eyes": "blue",
            "hair": "blonde",
            "skin": "fair",
            "figure": "slim",
        },
        "profession": "Waitress",
        "profile_image": SimpleUploadedFile(
            "Nicole.jpg", image_content[2], content_type="image/jpeg"
        ),
        "bio": "Bio for Nicole",
    }
    profile4_data = {
        "name": "Shenguang",
        "gender": "F",
        "age": 24,
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
            "Carla.jpg", image_content[3], content_type="image/jpeg"
        ),
        "bio": "Lorem ipsum",
    }

    # Create the two BotProfile instances using the data
    BotProfile.objects.all().delete()
    BotProfile(**profile1_data).save()
    BotProfile(**profile2_data).save()
    BotProfile(**profile3_data).save()
    BotProfile(**profile4_data).save()

    return JsonResponse({"status": "ok"})
