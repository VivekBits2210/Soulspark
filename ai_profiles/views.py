import base64
from django.http import HttpResponse
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from chat_module.models import ChatHistory
from .models import BotProfile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BotProfileSerializer

@api_view(['GET'])
def index(request):
    return HttpResponse("You are at the AI profiles index.")

@api_view(['GET'])
def fetch_profile(request):
    bot_id = int(request.GET.get('bot_id'))
    image_only = request.GET.get('image_only')

    # If the 'bot_id' parameter is provided, filter by bot_id
    if bot_id:
        query_set = BotProfile.objects.filter(bot_id=bot_id)
        if not query_set.exists():
            return JsonResponse({'error': f"No profile found for bot_id '{bot_id}'"})
        profile = query_set.first()
    else:
        profile = BotProfile.objects.order_by('?').first()

    image_data = profile.profile_image.read()
    if image_only:
        # Return the profile image as an HTTP response
        response = HttpResponse(image_data, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{profile.profile_image.name}"'
        return response

    encoded_image = base64.b64encode(image_data).decode('utf-8')

    # serialize the BotProfile object to a JSON response
    profile_data = {
        'bot_id': profile.bot_id,
        'gender': profile.gender,
        'age': profile.age,
        'profession': profile.profession,
        'hobbies': profile.hobbies,
        'favorites': profile.favorites,
        'profile_image_url': profile.profile_image.url,
        "profile_image": encoded_image,
    }
    return JsonResponse(profile_data)


@api_view(['POST'])
def create_profile_admin(request):
    serializer = BotProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: This api should also change the bot mapping in the chat history table
@login_required()
@api_view(['POST'])
def create_profile(request):
    bot_id = request.data.get('bot_id')
    name = request.data.get('name')
    gender = request.data.get('gender')
    age = request.data.get('age')
    profession = request.data.get('profession')
    hobbies = request.data.get('hobbies')
    favorites = request.data.get('favorites')
    profile_image = request.data.get('profile_image')

    original_bot = get_object_or_404(BotProfile, pk=bot_id)
    bot = original_bot.copy()

    if name:
        bot.name = name
    if gender:
        bot.gender = gender
    if age:
        bot.age = age
    if profession:
        bot.profession = profession
    if hobbies:
        bot.hobbies = hobbies
    if favorites:
        bot.favorites = favorites
    if profile_image:
        bot.profile_image = profile_image

    bot.save()
    ChatHistory.objects.create(user=request.user, bot=bot, history={}).save()
    return Response({"message": "BotProfile updated successfully!"})


# Usage for above api
# import requests

# data = {
#     'bot_id': 'my_bot',
#     'gender': 'F',
#     'age': 30,
#     'profession': 'Software engineer',
#     'hobbies': ['reading', 'hiking'],
#     'favorites': {'color': 'blue', 'food': 'pizza'},
#     'profile_image': open('/path/to/image.jpg', 'rb')
# }
#
# response = requests.post('http://localhost:8000/api/profiles/', data=data)
# print(response.json())
