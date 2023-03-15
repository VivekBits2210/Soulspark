import base64

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import UserProfile


def get_gender_list(gender_focus):
    if gender_focus == 'M':
        return ['M']
    elif gender_focus == 'F':
        return ['F']
    elif gender_focus == 'E':
        return ['M', 'F']


@api_view(["GET"])
@login_required
def fetch_profile(request):
    user = request.user
    n = request.GET.get("n")
    bot_id = request.GET.get("bot_id")
    no_image = request.GET.get("no_image")
    image_only = request.GET.get("image_only")

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        profile = UserProfile.objects.create(user=user)
    else:
        profile = profile_queryset.first()

    if n:
        try:
            n = int(n)
        except ValueError:
            return JsonResponse(
                {"error": f"Invalid value for 'n': {n}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        gender_list = get_gender_list(profile.gender_focus)
        query_set = BotProfile.objects.filter(searchable=True, gender__in=gender_list).order_by("?")[:n]
        output_list = []
        for profile in query_set:
            output_dict = model_to_dict(profile)
            if no_image:
                del output_dict["profile_image"]
            else:
                image_data = profile.profile_image.read()
                encoded_image = base64.b64encode(image_data).decode("utf-8")
                output_dict = model_to_dict(profile)
                output_dict["profile_image"] = encoded_image
            output_list.append(output_dict)

        return JsonResponse(output_list, status=status.HTTP_200_OK, safe=False)

    # If the 'bot_id' parameter is provided, filter by bot_id
    if bot_id:
        try:
            bot_id = int(bot_id)
        except ValueError:
            return JsonResponse(
                {"error": f"Bot ID {bot_id} is not an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        query_set = BotProfile.objects.filter(bot_id=bot_id)
        if not query_set.exists():
            return JsonResponse(
                {"error": f"No profile found for bot_id '{bot_id}'"},
                status=status.HTTP_404_NOT_FOUND,
            )
        profile = query_set.first()
    else:
        profile = BotProfile.objects.order_by("?").first()

    if no_image:
        output_dict = model_to_dict(profile)
        del output_dict["profile_image"]
        return JsonResponse(output_dict, status=status.HTTP_200_OK)

    image_data = profile.profile_image.read()
    if image_only:
        response = HttpResponse(
            image_data, content_type="image/jpeg", status=status.HTTP_200_OK
        )
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{profile.profile_image.name}"'
        return response

    encoded_image = base64.b64encode(image_data).decode("utf-8")
    output_dict = model_to_dict(profile)
    output_dict["profile_image"] = encoded_image
    return JsonResponse(output_dict, status=status.HTTP_200_OK)
