from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict

from chat_module.models import UserProfile

@login_required
@api_view(['GET'])
def fetch_user_info(request):
    user = request.user
    email = EmailAddress.objects.filter(user=user).first()
    social_account = SocialAccount.objects.filter(user=user).first()
    profile_queryset = UserProfile.objects.filter(user=user)

    if not profile_queryset.exists():
        profile = UserProfile.objects.create(user=user)
        profile.save()
    else:
        profile = profile_queryset.first()

    user_profile = model_to_dict(profile)
    user_profile['uid'] =  social_account.uid if social_account else None
    user_profile['email'] = email.email if email else None
    return JsonResponse(user_profile, safe=False)
