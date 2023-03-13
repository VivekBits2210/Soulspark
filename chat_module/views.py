from django.shortcuts import render

# Create your views here.
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
