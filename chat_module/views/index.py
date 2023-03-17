from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import render


@api_view(["GET"])
def index(request):
    return HttpResponse("You are at the chat module index.")


class ChatView(APIView):
    def get(self, request):
        return render(request, "chat/chat.html")
    # template_name: str = "chat/chat.html"


