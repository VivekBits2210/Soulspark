from django.urls import path
from ai_profiles.views import create_profile, create_profile_admin, fetch_profile, index

urlpatterns = [
    path('', index.index, name='index'),
    path('create-profile-admin', create_profile_admin.create_profile_admin, name=''),
    path('create-profile', create_profile.create_profile, name=''),
    path('fetch-profile', fetch_profile.fetch_profile, name=''),
]