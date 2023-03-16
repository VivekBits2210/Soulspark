import json
import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ai_profiles.models import BotProfile
from chat_module.models import ChatHistory


class UnmatchTestCase(APITestCase):
    pass
