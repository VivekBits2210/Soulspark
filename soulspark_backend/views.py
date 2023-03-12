from django.http import HttpResponse
from PIL import Image
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Soulspark Index Page: Logged out users can see /ai-profiles, Logged in users can see /ai-profiles/generate-images")
