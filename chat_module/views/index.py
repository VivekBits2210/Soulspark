from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import render

from django.views.generic import TemplateView


##todo: you can get rid of this func
@api_view(["GET"])
def index(request):
    return HttpResponse("You are at the chat module index.")


class ChatView(APIView):
    def get(self, request):
        ## todo: query chat history and pass to chat.html
        return render(request, "chat/chat.html")
