from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict

from user_profiles.models import UserProfile, User
from user_profiles.utils import decrypt_email


@api_view(["GET"])
def fetch_user_info(request):
    encrypted_email = request.GET.get('email')
    email = decrypt_email(encrypted_email)

    try:
        user = User.objects.get(pk=email)
    except User.DoesNotExist:
        error_message = {'error': f'User {encrypted_email} not found'}
        return JsonResponse(error_message, status=status.HTTP_404_NOT_FOUND)

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
