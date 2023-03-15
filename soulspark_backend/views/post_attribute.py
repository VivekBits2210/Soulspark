import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from chat_module.models import UserProfile


# TODO: Check if the attribute sent in is a valid settable attribute
@login_required
@api_view(["POST"])
def post_attribute(request):
    user = request.user
    data = json.loads(request.body.decode("utf-8"))
    key = data["key"]
    value = data["value"]

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        try:
            profile = UserProfile.objects.create(user=user)
        except ValidationError as e:
            return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST)
    else:
        profile = profile_queryset.first()

    try:
        setattr(profile, key, value)
        profile.save()
    except ValidationError as e:
        return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({key: value}, status=status.HTTP_200_OK)
