from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from user_profiles.serializers import UserSerializer
from user_profiles.utils import decrypt_email


@api_view(["POST"])
def create_user(request):
    request_dict = request.data

    try:
        request_dict['email'] = decrypt_email(request_dict['email'])
    except KeyError:
        return JsonResponse({'error': 'email parameter missing'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request_dict)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        serializer.save()
    except ValidationError as e:
        return JsonResponse({'error': repr(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
