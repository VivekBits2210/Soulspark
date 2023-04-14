from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from user_profiles.models import UserProfile
from user_profiles.utils import fetch_user_or_error
import logging

logger = logging.getLogger("my_logger")


def get_gender_list(gender_focus):
    if gender_focus == "M":
        return ["M"]
    elif gender_focus == "F":
        return ["F"]
    elif gender_focus == "E":
        return ["M", "F"]


@api_view(["GET"])
def fetch_profile(request):
    logger.info("Logging line from fetch_profile")
    n = request.GET.get("n")
    bot_profile_id = request.GET.get("bot_profile_id")

    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    gender_focus = UserProfile.objects.get(user=user_or_error).gender_focus
    if not gender_focus:
        gender_focus = "E"

    if n:
        try:
            n = int(n)
        except ValueError:
            return JsonResponse(
                {"error": f"Invalid value for 'n': {n}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        gender_list = get_gender_list(gender_focus)
        query_set = BotProfile.objects.filter(
            searchable=True, gender__in=gender_list
        ).order_by("?")[:n]
        output_list = []
        for profile in query_set:
            output_dict = model_to_dict(profile)
            output_list.append(output_dict)

        return JsonResponse(output_list, status=status.HTTP_200_OK, safe=False)

    # If the 'bot_profile_id' parameter is provided, filter by bot_profile_id
    if bot_profile_id:
        try:
            bot_profile_id = int(bot_profile_id)
        except ValueError:
            return JsonResponse(
                {"error": f"Bot ID {bot_profile_id} is not an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        query_set = BotProfile.objects.filter(bot_profile_id=bot_profile_id)
        if not query_set.exists():
            return JsonResponse(
                {"error": f"No profile found for bot_profile_id '{bot_profile_id}'"},
                status=status.HTTP_404_NOT_FOUND,
            )
        profile = query_set.first()
    else:
        profile = BotProfile.objects.order_by("?").first()

    output_dict = model_to_dict(profile)
    return JsonResponse(output_dict, status=status.HTTP_200_OK)
