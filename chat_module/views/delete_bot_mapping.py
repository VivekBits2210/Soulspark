# TODO: call this api when unmatching
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

#TODO: Fill
@login_required
@api_view(['POST'])
def delete_bot_mapping(request):
    pass