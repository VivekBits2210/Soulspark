import base64
from django.http import HttpResponse
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import BotProfile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BotProfileSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the AI profiles index.")


# TODO: Remove this login_required (only used for temporary testing of auth)
@login_required
def generate_profile(request):
    image = Image.new('RGB', (200, 200), (255, 0, 0))
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response


def fetch_profile(request):
    bot_id = request.GET.get('bot_id')
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
def create_profile(request):
    serializer = BotProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
