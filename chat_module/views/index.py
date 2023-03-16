from django.http import HttpResponse
from rest_framework.decorators import api_view

from django.views.generic import TemplateView


@api_view(["GET"])
def index(request):
    return HttpResponse("You are at the chat module index.")


class ChatView(TemplateView):
    template_name: str = "chat/chat.html"


