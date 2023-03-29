from django.urls import path
from ai_profiles.views import (
    customize_profile,
    create_profile_admin,
    fetch_profile_admin,
    fetch_profile,
    index,
)

urlpatterns = [
    path("", index.index, name="ai_profiles_index"),
    path(
        "create-profile-admin",
        create_profile_admin.create_profile_admin,
        name="create_profile_admin",
    ),
    path(
        "customize-profile",
        customize_profile.customize_profile,
        name="customize_profile",
    ),
    path("fetch-profile", fetch_profile.fetch_profile, name="fetch_profile"),
]
