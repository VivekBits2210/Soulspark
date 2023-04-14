from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from user_profiles.models import UserProfile
from user_profiles.utils import fetch_user_or_error


@api_view(["POST"])
def post_attribute(request):
    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        try:
            profile = UserProfile.objects.create(user=user, gender_focus='E')
        except ValidationError as e:
            return JsonResponse({"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        profile = profile_queryset.first()

    profile_fields = set([f.name for f in UserProfile._meta.get_fields() if f.concrete])

    request_dict = request.data
    request_dict._mutable = True
    del request_dict["email"]

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
            if key == "name":
                user.first_name = request_dict["name"]
                user.save()
        profile.save()
    except ValidationError as e:
        return JsonResponse({"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse(model_to_dict(profile), status=status.HTTP_200_OK)
