from django.urls import path
from user_profiles.views import fetch_user_info, post_attribute, create_user, post_feedback

urlpatterns = [
    path("create-user", create_user.create_user, name="create_user"),
    path("fetch-user-info", fetch_user_info.fetch_user_info, name="fetch_user_info"),
    path("post-attribute", post_attribute.post_attribute, name="post_attribute"),
    path("post-feedback", post_feedback.post_feedback, name="post_feedback"),
]
