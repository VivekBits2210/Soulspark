from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict

from user_profiles.models import UserProfile, User
from user_profiles.utils import decrypt_email, fetch_user_or_error


@api_view(["GET"])
def fetch_user_info(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        try:
            profile = UserProfile.objects.create(user=user)
        except ValidationError as e:
            return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST)
    else:
        profile = profile_queryset.first()

    user_profile = model_to_dict(profile)
    return JsonResponse(user_profile, safe=False, status=status.HTTP_200_OK)
