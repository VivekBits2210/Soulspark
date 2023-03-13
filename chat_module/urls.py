from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-user-info', views.fetch_user, name='fetch-user-info'),
]