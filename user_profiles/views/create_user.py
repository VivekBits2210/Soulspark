from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from user_profiles.serializers import UserSerializer
from user_profiles.utils import decrypt_email


@api_view(["POST"])
def create_user(request):
    request_dict = request.data

    request_dict['email'] = decrypt_email(request_dict['email'])
    serializer = UserSerializer(data=request_dict)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
