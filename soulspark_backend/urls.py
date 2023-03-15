from django.contrib import admin
from django.urls import include, path
from soulspark_backend.views import clear_db, fetch_user_info, fill_db, post_attribute
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SoulSpark API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("post-attribute", post_attribute.post_attribute, name="post-attribute"),
    path("fetch-user-info", fetch_user_info.fetch_user_info, name="fetch-user-info"),
    path("fill-db", fill_db.fill_db, name="fill-db"),
    path("clear-db", clear_db.clear_db, name="clear-db"),
    path("ai-profiles/", include("ai_profiles.urls")),
    path("chat-module/", include("chat_module.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
]
