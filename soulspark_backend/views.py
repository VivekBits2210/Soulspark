from django.http import HttpResponse

def index(request):
    return HttpResponse("Soulspark Index Page")
