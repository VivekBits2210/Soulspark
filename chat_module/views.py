
# Create your views here.
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import UserProfile
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount


def index(request):
    return HttpResponse("You are at the chat module index.")


@login_required
def fetch_user(request):
    user = request.user
    print(request.user)
    email = EmailAddress.objects.filter(user=user).first()
    social_account = SocialAccount.objects.filter(user=user).first()
    profile = UserProfile.objects.filter(UID=social_account.uid).first()

    # Create a dictionary with the combined user profile information
    user_profile = {
        'UID': profile.UID,
        'username': user.username,
        'email': email.email,
        'age': profile.age,
        'gender': profile.gender,
        'level': profile.level,
    }

    return JsonResponse(user_profile, safe=False)


@login_required
@csrf_exempt
@require_POST
def post_message(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    message = data['message']
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)('chatbot', {'uid': user, 'bot_id': data['bot_id'], 'message': message})

    return JsonResponse({'status': 'ok'})
