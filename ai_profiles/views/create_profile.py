from copy import deepcopy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory


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

    original_bot = BotProfile.objects.get(bot_id=bot_id)
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
    if profile_image:
        bot.profile_image = profile_image

    bot.save()
    ChatHistory.objects.create(user=request.user, bot=bot, history={}).save()
    return JsonResponse({"message": f"{bot.get_id()} bot updated successfully!"})
