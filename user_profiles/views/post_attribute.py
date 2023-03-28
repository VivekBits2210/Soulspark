from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from user_profiles.models import UserProfile, User
from user_profiles.utils import decrypt_email


@api_view(["POST"])
def post_attribute(request):
    encrypted_email = request.GET.get('email')
    email = decrypt_email(encrypted_email)

    try:
        user = User.objects.get(pk=email)
    except User.DoesNotExist:
        error_message = {'error': f'User {encrypted_email} not found'}
        return JsonResponse(error_message, status=status.HTTP_404_NOT_FOUND)

    request_dict = request.data

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        try:
            profile = UserProfile.objects.create(user=user)
        except ValidationError as e:
            return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST)
    else:
        profile = profile_queryset.first()

    profile_fields = set([f.name for f in UserProfile._meta.get_fields() if f.concrete])

    incorrect_attributes = [
        key for key in request_dict.keys() if key not in profile_fields
    ]
    if len(incorrect_attributes) > 0:
        return JsonResponse(
            {
                "error": f"Attributes {incorrect_attributes} are not valid UserProfile attributes"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        for key in request_dict.keys():
            setattr(profile, key, request_dict[key])
        profile.save()
    except ValidationError as e:
        return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse(model_to_dict(profile), status=status.HTTP_200_OK)
