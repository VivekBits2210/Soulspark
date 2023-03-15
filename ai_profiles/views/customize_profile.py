from copy import deepcopy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory


@login_required()
@api_view(['POST'])
def customize_profile(request):
    bot_id = request.data.get('bot_id')
    name = request.data.get('name')
    gender = request.data.get('gender')
    age = request.data.get('age')
    profession = request.data.get('profession')
    hobbies = request.data.get('hobbies')
    favorites = request.data.get('favorites')

    if not bot_id:
        return JsonResponse({'error': f"No bot_id given"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        bot_id = int(bot_id)
    except ValueError:
        return JsonResponse({'error': f"{bot_id} is not an integer."}, status=status.HTTP_400_BAD_REQUEST)
    bot_queryset = BotProfile.objects.filter(bot_id=bot_id)
    if not bot_queryset.exists():
        return JsonResponse({'error': f"bot {bot_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    original_bot = bot_queryset.first()
    bot = deepcopy(original_bot)

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

    # TODO: Fill history from before, shouldn't be empty here!
    try:
        bot.save()
        ChatHistory.objects.create(user=request.user, bot=bot, history={}).save()
        return JsonResponse({"message": f"{bot.get_id()} bot updated successfully!"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return JsonResponse(repr(e), status=status.HTTP_400_BAD_REQUEST)