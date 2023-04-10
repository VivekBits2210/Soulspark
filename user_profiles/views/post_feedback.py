from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from user_profiles.models.feedback import UserFeedback
from user_profiles.utils import fetch_user_or_error


@api_view(["POST"])
def post_feedback(request):
    request_dict = request.data
    if 'feedback' not in request_dict:
        return JsonResponse(
            {"error": "feedback key not found"}, status=status.HTTP_400_BAD_REQUEST
        )

    user_or_error = fetch_user_or_error(request)
    if isinstance(user_or_error, JsonResponse):
        error_response = user_or_error
        return error_response
    user = user_or_error
    UserFeedback.objects.create(user=user, feedback=request_dict['feedback'])

    return JsonResponse(
        {"message": f"Feedback stored"},
        status=status.HTTP_200_OK,
    )