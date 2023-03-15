# TODO: Remove these dangerous apis once the models have evolved well enough
from allauth.socialaccount.models import SocialApp
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import UserProfile


@api_view(["GET"])
def clear_db(request):
    db = request.GET.get("db")
    if db == "bot":
        BotProfile.objects.all().delete()
    elif db == "user":
        UserProfile.objects.all().delete()
    elif db == "all":
        SocialApp.objects.all().delete()
        BotProfile.objects.all().delete()
        UserProfile.objects.all().delete()
    return JsonResponse({"status": "ok"})
