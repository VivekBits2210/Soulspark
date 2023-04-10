from django.urls import path
from chat_module.views import (
    index,
    fetch_chat_history,
    unmatch,
    fetch_selected_profiles,
    fetch_level,
    delete_all_chat_history
)

urlpatterns = [
    path(
        "fetch-selected-profiles",
        fetch_selected_profiles.fetch_selected_profiles,
        name="fetch_selected_profiles",
    ),
    path(
        "fetch-chat-history",
        fetch_chat_history.fetch_chat_history,
        name="fetch_chat_history",
    ),
    path(
        "fetch-level",
        fetch_level.fetch_level,
        name="fetch_level",
    ),
    path("unmatch", unmatch.unmatch, name="unmatch"),
    path("delete-all-chat-history", delete_all_chat_history.delete_all_chat_history),
    path("", index.ChatView.as_view(), name="chat_view"),
]
