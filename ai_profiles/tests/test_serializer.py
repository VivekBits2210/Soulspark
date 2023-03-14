import os
import io
from unittest import skip

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from ai_profiles.serializers import BotProfileSerializer


class BotProfileSerializerTestCase(APITestCase):
    def setUp(self):
        image_path = os.path.join('static', 'trial.jpg')
        with open(image_path, 'rb') as f:
            image_content = f.read()

        # Create a SimpleUploadedFile object from the image content
        self.valid_data = {
            'name': 'Bot',
            'gender': 'M',
            'age': 30,
            'bio': 'I am Bot1',
            'profession': 'Engineer',
            'hobbies': {'hobbies':['chess','cricket']},
            'physical_attributes': {"hair":"black"},
            'favorites': {'color': 'blue', 'food': 'pizza'},
            'profile_image': SimpleUploadedFile("test_serializer.jpg", image_content, content_type="image/jpeg")
        }

    def test_create_valid_bot_profile(self):
        serializer = BotProfileSerializer(data=self.valid_data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        profile = serializer.save()
        self.assertIsNotNone(profile.bot_id)
        self.assertEqual(profile.name, self.valid_data['name'])
        self.assertEqual(profile.gender, self.valid_data['gender'])
        self.assertEqual(profile.age, self.valid_data['age'])
        self.assertEqual(profile.bio, self.valid_data['bio'])
        self.assertEqual(profile.profession, self.valid_data['profession'])
        self.assertEqual(profile.hobbies, self.valid_data['hobbies'])
        self.assertEqual(profile.favorites, self.valid_data['favorites'])
        self.assertIsNotNone(profile.profile_image)

    def test_missing_required_fields(self):
        invalid_data = {
            'name': 'Bot1',
            'gender': 'M',
            'age': 30,
        }
        serializer = BotProfileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'name', 'physical_attributes', 'bio', 'profession', 'hobbies', 'favorites','profile_image'})

    @skip
    def test_invalid_profile_image(self):
        invalid_data = self.valid_data.copy()
        invalid_data['profile_image'] = SimpleUploadedFile("test_image.txt", b"file_content", content_type="text/plain")
        serializer = BotProfileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'profile_image'})

    @skip
    def test_profile_image_resized(self):
        # create a test image with dimensions larger than 100x100
        file = io.BytesIO()
        image = Image.new('RGB', (200, 200), 'white')
        image.save(file, 'jpeg')
        file.name = 'test_image.jpg'
        file.seek(0)
        invalid_data = self.valid_data.copy()
        invalid_data['profile_image'] = SimpleUploadedFile(file.name, file.read(), content_type="image/jpeg")
        serializer = BotProfileSerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())
        profile = serializer.save()
        self.assertEqual(profile.profile_image.width, 100)
        self.assertEqual(profile.profile_image.height, 100)

    def tearDown(self):
        # remove all text files and files starting with 'trial' under the 'images' folder
        folder_path = os.path.join('images')
        to_remove = []
        for filename in os.listdir(folder_path):
            if filename.startswith('test'):
                file_path = os.path.join(folder_path, filename)
                to_remove.append(file_path)

        for path in to_remove:
            os.remove(path)

        super().tearDown()