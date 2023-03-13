"""soulspark_backend URL Configuration
"""
from django.contrib import admin
from django.urls import include, path, re_path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SoulSpark API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
urlpatterns = [
    path('post-attribute', views.post_attribute, name='post-attribute'),
    path('post-age', views.post_age, name='post-age'),
    path('post-gender', views.post_gender, name='post-gender'),
    path('post-gender-focus', views.post_gender_focus, name='post-gender-focus'),
    path('post-interests', views.post_interests, name='post-interests'),
    path('fetch-user-info', views.fetch_user, name='fetch-user-info'),
    path('fill-db', views.fill_db, name='fill-db'),

    path('ai-profiles/', include('ai_profiles.urls')),
    path('chat-module/', include('chat_module.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    re_path(r'', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]