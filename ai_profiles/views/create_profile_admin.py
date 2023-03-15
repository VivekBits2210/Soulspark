import os

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ai_profiles.serializers import BotProfileSerializer


@api_view(["POST"])
def create_profile_admin(request):
    input_data = dict(request.data)
    image_path = os.path.join("static", input_data["profile_image"])
    with open(image_path, "rb") as f:
        image_content = f.read()
    image_file = SimpleUploadedFile(
        input_data["profile_image"], image_content, content_type="image/jpeg"
    )
    input_data["profile_image"] = image_file

    serializer = BotProfileSerializer(data=input_data)
    if serializer.is_valid():
        try:
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse(dict(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
