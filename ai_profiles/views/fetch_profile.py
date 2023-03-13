import base64
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile


@api_view(['GET'])
def fetch_profile(request):
    bot_id = request.GET.get('bot_id')
    image_only = request.GET.get('image_only')

    # If the 'bot_id' parameter is provided, filter by bot_id
    if bot_id:
        query_set = BotProfile.objects.filter(bot_id=int(bot_id))
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