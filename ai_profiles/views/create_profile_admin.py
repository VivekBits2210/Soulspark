from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.serializers import BotProfileSerializer


@api_view(['POST'])
def create_profile_admin(request):
    serializer = BotProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
