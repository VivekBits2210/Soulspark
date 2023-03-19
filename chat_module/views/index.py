from rest_framework.views import APIView
from django.shortcuts import render


class ChatView(APIView):
    def get(self, request):
        ## TODO: query chat history and pass to chat.html
        return render(request, "chat/chat.html")
