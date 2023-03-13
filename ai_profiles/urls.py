from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-profile-admin', views.create_profile_admin, name=''),
    path('create-profile', views.create_profile, name=''),
    path('fetch-profile', views.fetch_profile, name=''),
]