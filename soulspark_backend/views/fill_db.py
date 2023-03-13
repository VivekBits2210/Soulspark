# TODO: Remove these dangerous apis once the models have evolved well enough
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ai_profiles.models import BotProfile
from chat_module.models import UserProfile


@api_view(['GET'])
def fill_db(request):
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