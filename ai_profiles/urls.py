from django.urls import path
from ai_profiles.views import (
    customize_profile,
    fetch_profile,
    index,
)

urlpatterns = [
    path("", index.index, name="ai_profiles_index"),
    path(
        "customize-profile",
        customize_profile.customize_profile,
        name="customize_profile",
    ),
    path("fetch-profile", fetch_profile.fetch_profile, name="fetch_profile"),
]
