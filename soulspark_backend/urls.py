"""soulspark_backend URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ai-profiles/', include('ai_profiles.urls')),
    path('chat-module/', include('chat_module.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]