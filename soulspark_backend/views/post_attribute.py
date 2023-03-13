import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from chat_module.models import UserProfile


@login_required
@api_view(['POST'])
def post_attribute(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    key = data['key']
    value = data['value']

    profile_queryset = UserProfile.objects.filter(user=user)
    if not profile_queryset.exists():
        profile = UserProfile.objects.create(user=user)
    else:
        profile = profile_queryset.first()
    setattr(profile, key, value)
    profile.save()
    return JsonResponse({'status': 'ok'})