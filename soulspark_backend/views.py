import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view

from chat_module.models import UserProfile

#WARNING: Use post_attributes instead of these APIs, these are not registered under urls.
@login_required
@api_view(['GET'])
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
@api_view(['GET'])
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
@api_view(['GET'])
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
@api_view(['GET'])
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
