import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import UserProfile

@api_view(['GET'])
def index(request):
    return HttpResponse("Soulspark Index Page")


@login_required
@api_view(['GET'])
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


# TODO: Remove these dangerous apis once the models have evolved well enough
@api_view(['GET'])
def fill_db(request):
    # Site.objects.all().delete()
    SocialApp.objects.all().delete()
    queryset = Site.objects.filter(name='localhost')
    if not queryset.exists():
        site = Site.objects.create(domain='localhost:8000', name='localhost')
        site.save()
    else:
        site = queryset.first()

    provider = 'google'
    name = 'Google SSO'
    client_id = '485503899387-03u1pvv94g1k01tf9rhv7nno51tbfmls.apps.googleusercontent.com'
    secret = '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'
    key = ''

    social_app = SocialApp.objects.create(provider=provider,
                                          name=name,
                                          client_id=client_id,
                                          secret=secret,
                                          key=key)
    social_app.sites.add(Site.objects.filter(name='localhost').first())
    social_app.save()

    profile1_data = {
        'name': 'Nicole',
        'gender': 'F',
        'age': 18,
        'hobbies': ['reading', 'painting'],
        'favorites': {'color': 'red', 'food': 'pizza'},
        'profession': 'Air hostess',
        'profile_image': '/static/trial1.jpg',
        'bio': 'Lorem ipsum'
    }
    profile2_data = {
        'name': 'Carla',
        'gender': 'F',
        'age': 25,
        'hobbies': ['hiking', 'yoga'],
        'favorites': {'color': 'blue', 'food': 'sushi'},
        'profession': 'Secretary',
        'profile_image': '/static/trial2.jpg',
        'bio': 'Lorem ipsum'
    }

    # Create the two BotProfile instances using the data
    BotProfile.objects.all().delete()
    UserProfile.objects.all().delete()
    profile1 = BotProfile(**profile1_data)
    profile2 = BotProfile(**profile2_data)

    # Save the profiles to the database
    profile1.save()
    profile2.save()
    return JsonResponse({'status': 'ok'})


# TODO: Remove these dangerous apis once the models have evolved well enough
@api_view(['GET'])
def clear_db(request):
    db = int(request.GET.get('db'))
    if db == 'bot':
        BotProfile.objects.all().delete()
    elif db == 'user':
        UserProfile.objects.all().delete()
    elif db == 'all':
        SocialApp.objects.all().delete()
        BotProfile.objects.all().delete()
        UserProfile.objects.all().delete()
    return JsonResponse({'status': 'ok'})
