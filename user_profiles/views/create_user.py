from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(["POST"])
def create_user(request):
    request_dict = request.data
    request_dict["notifying_key"] = "Rahul_Raj"
    return JsonResponse(request_dict, safe=False, status=status.HTTP_200_OK)
