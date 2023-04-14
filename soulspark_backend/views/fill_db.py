import os

from django.http import JsonResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile


@api_view(["GET"])
def fill_db(request):
    profile1_data = {
        "name": "Nicole",
        "gender": "F",
        "age": 18,
        "interests": "reading and running",
        "favorites": {"color": "red", "food": "pizza"},
        "physical_attributes": {"eyes": "blue"},
        "profession": "Air hostess",
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
        "bio": "Lorem ipsum",
    }

    profile5_data = {
        "name": "Ivan",
        "gender": "M",
        "age": 25,
        "interests": "baking and studying",
        "favorites": {"color": "scarlet", "food": "chicken biryani"},
        "physical_attributes": {},
        "profession": "PhD student",
        "bio": "I am Ivan",
    }

    # Create the two BotProfile instances using the data
    BotProfile.objects.all().delete()
    BotProfile(**profile1_data).save()
    BotProfile(**profile2_data).save()
    BotProfile(**profile3_data).save()
    BotProfile(**profile4_data).save()
    BotProfile(**profile5_data).save()

    return JsonResponse({"status": "ok"})
