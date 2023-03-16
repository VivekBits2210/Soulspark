from django.urls import path
from chat_module.views import index, fetch_chat_history, unmatch

urlpatterns = [
    # path("", index.index, name="chat_module_index"),
    path(
        "fetch-chat-history",
        fetch_chat_history.fetch_chat_history,
        name="fetch_chat_history",
    ),
    path("unmatch", unmatch.unmatch, name="unmatch"),
    path("", index.ChatView.as_view(), name="chat_view"),
]
