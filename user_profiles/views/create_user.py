from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from user_profiles.models import User, UserProfile
from user_profiles.serializers import UserSerializer
from user_profiles.utils import decrypt_email


@api_view(["POST"])
def create_user(request):
    request_dict = request.data

    try:
        decrypted_email = decrypt_email(request_dict["email"])
        if User.objects.filter(email=decrypted_email):
            return JsonResponse(model_to_dict(User.objects.get(email=decrypted_email)), status=status.HTTP_200_OK)
    except KeyError:
        return JsonResponse(
            {"error": "email parameter missing"}, status=status.HTTP_400_BAD_REQUEST
        )
    except ValueError as e:
        return JsonResponse({"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        serializer = UserSerializer(data={
            "email":decrypted_email,
            "first_name": request_dict["first_name"],
            "last_name": request_dict["last_name"],
            "picture": request_dict["picture"],
        })
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        UserProfile.objects.create(user=serializer.instance, gender_focus="E")
    except Exception as e:
        return JsonResponse({"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
