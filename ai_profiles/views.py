from django.http import HttpResponse
from PIL import Image
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, world. You're at the AI profiles index.")

@login_required
def generate_images(request):
    image = Image.new('RGB', (200, 200), (255, 0, 0))
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response
