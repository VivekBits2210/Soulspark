from django.http import HttpResponse
from PIL import Image


def index(request):
    return HttpResponse("Hello, world. You're at the AI profiles index.")


def generate_images(request):
    image = Image.new('RGB', (200, 200), (255, 0, 0))
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response
