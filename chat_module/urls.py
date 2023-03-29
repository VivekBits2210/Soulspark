from django.urls import path
from chat_module.views import index, fetch_chat_history, unmatch
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path("", index.index, name="chat_module_index"),
    path(
        "fetch-chat-history",
        fetch_chat_history.fetch_chat_history,
        name="fetch_chat_history",
    ),
    path("unmatch", unmatch.unmatch, name="unmatch"),
    path("", login_required(index.ChatView.as_view()), name="chat_view"),
]
