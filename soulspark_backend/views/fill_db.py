import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from user_profiles.utils import decrypt_email


@api_view(["GET"])
def fill_db(request):
    try:
        encrypted_email = request.GET.get("email")
    except KeyError:
        return JsonResponse(
            {"error": "email parameter missing"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not encrypted_email:
        return JsonResponse(
            {"error": "email parameter missing"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        email = decrypt_email(encrypted_email)
    except ValueError as e:
        return JsonResponse({"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST)

    if email != "arbitraryemail@email.com":
        return JsonResponse(
            {"error": "Unauthorized access"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Create the two BotProfile instances using the data
    BotProfile.objects.all().delete()
    json_file_path = "./soulspark_backend/profiles.json"

    with open(json_file_path, 'r') as j:
        profiles = json.loads(j.read())
        for profile in profiles:
            bot = BotProfile(**profile)
            bot.bot_profile_id = bot.name
            bot.save()

    return JsonResponse({"profiles": len(BotProfile.objects.filter())})
