from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate-profile', views.generate_profile, name=''),
    path('fetch-profile', views.fetch_profile, name=''),
]