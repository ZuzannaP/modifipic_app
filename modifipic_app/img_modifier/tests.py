import json
import os

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status, response
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


from .models import TheImage
from .serializers import ImageSerializer

from django.test import override_settings
import shutil

TEST_DIR = 'test_data'
my_media_root = os.path.join(TEST_DIR, 'media')

"""
formularz!!!

serializers
"""

class LoginTests(APITestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=(my_media_root))
    def setUp(cls):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        cls.the_image = TheImage.objects.create(file=image_mock)

    def test_loging_assertion_fail(self):
        c = Client()
        response = c.delete(f'/api/raw_images/{self.the_image.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_assertion_pass(self):
        test_user = User.objects.create_user(username="ms_test_user", password="ms_test_users_secret_password")
        c = Client()
        c.login(username="ms_test_user", password="ms_test_users_secret_password")
        response = c.delete(f'/api/raw_images/{self.the_image.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDownModule(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass


class SerializerTest(APITestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=(my_media_root))
    def setUp(cls):
        cls.random_photo = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        cls.the_image = TheImage.objects.create(file=cls.random_photo)
        cls.the_image_attributes = {
            'file': cls.the_image.file,
            'category': 0
        }
        cls.serializer = ImageSerializer(instance=cls.the_image)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['pk', 'file', 'category', 'upload_date'])

    def test_category_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['category'], str(self.the_image_attributes['category']))

    def test_file_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['file'], os.path.join("/media",str(self.the_image_attributes['file'])))

    def tearDownModule(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

# class RawImageViewSetTest(APITestCase):
#     @classmethod
#       @override_settings(MEDIA_ROOT=(my_media_root))
#     def setUpTestCase(cls):
#         cls.image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
#
#     def test_image_upload(self):
#         url = 'Raw Images View'
#         data = {'file': self.image_mock, 'category': 0}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(TheImage.objects.count(), 1)

    # def tearDownModule(self):
    #     try:
    #         shutil.rmtree(TEST_DIR)
    #     except OSError:
    #         pass


class BluredImageViewSetTest(APITestCase):
    pass

class FlippedHorizontallyImageViewSetTest(APITestCase):
    pass

class GrayImageViewSetTest(APITestCase):
    pass

class SepiaImageViewSetTest(APITestCase):
    pass

'''
class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')
'''
