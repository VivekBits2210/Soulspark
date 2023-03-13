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
    email = EmailAddress.objects.filter(user=user).first()
    social_account = SocialAccount.objects.filter(user=user).first()
    profile_queryset = UserProfile.objects.filter(user=user)

    if not profile_queryset.exists():
        profile = UserProfile.objects.create(user=user)
        profile.save()
    else:
        profile = profile_queryset.first()

    user_profile = {
        'uid': social_account.uid,
        'username': user.username,
        'email': email.email,
        'age': profile.age,
        'gender': profile.gender,
        'level': profile.level,
    }

    return JsonResponse(user_profile, safe=False)


@login_required
@require_POST
def post_age(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    age = int(data['age'])

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        profile = UserProfile.objects.create(user=user)
    else:
        profile = profile_queryset.first()
    profile.age = age
    profile.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def post_gender(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    gender = data['gender']

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        profile = UserProfile.objects.create(user=user)
    else:
        profile = profile_queryset.first()
    profile.gender = gender
    profile.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def post_gender_focus(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    gender_focus = data['gender_focus']

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        profile = UserProfile.objects.create(user=user)
    else:
        profile = profile_queryset.first()
    profile.gender_focus = gender_focus
    profile.save()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def post_interests(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    interests = data['interests']

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        profile = UserProfile.objects.create(user=user)
    else:
        profile = profile_queryset.first()
    profile.interests = interests
    profile.save()
    return JsonResponse({'status': 'ok'})


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
