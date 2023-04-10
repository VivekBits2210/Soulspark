from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from user_profiles.models import UserProfile
from user_profiles.utils import fetch_user_or_error


@api_view(["POST"])
def delete_user(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error
    email = user.email

    profile_queryset = UserProfile.objects.filter(user=user)
    profile_queryset.delete()
    user.delete()

    return JsonResponse(
        {"message": f"User {email} deleted"},
        status=status.HTTP_200_OK,
    )