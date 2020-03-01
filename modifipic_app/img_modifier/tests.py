import os

from django.contrib.auth.models import User
from django.core.files import File
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from .models import TheImage
from .serializers import ImageSerializer

from django.test import override_settings
import shutil


"""
BRAKI:
1. test formularza w innej apce
2. test dodania tu zdjecia
3 test przetesowania akcj np. blurr

"""


TEST_DIR = 'test_data'
my_media_root = os.path.join(TEST_DIR, 'media')

class LoginTests(APITestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=(my_media_root))
    def setUp(cls):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        cls.the_image = TheImage.objects.create(file=image_mock)

    def test_loging_assertion_fail(self):
        c = APIClient()
        response = c.delete(f'/api/raw_images/{self.the_image.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_assertion_pass(self):
        test_user = User.objects.create_user(username="ms_test_user", password="ms_test_users_secret_password")
        c = APIClient()
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
        cls.random_photo = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpeg')
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
#

# class RawImageViewSetTest(APITestCase):
#     @classmethod
#     @override_settings(MEDIA_ROOT=(my_media_root))
#     def setUp(cls):
#         cls.image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpeg')
#         cls.client = APIClient()
#
# # how to upload a file?
#     def test_image_upload(self):
#         url = '/api/raw_images/'
#         data = {'file': self.image_mock, 'category': 0}
#         response = self.client.post(url, data, format='multipart')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(TheImage.objects.count(), 1)
#
#     def tearDownModule(self):
#         try:
#             shutil.rmtree(TEST_DIR)
#         except OSError:
#             pass


class BluredImageViewTest(APITestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=(my_media_root))
    def setUp(cls):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        cls.the_image = TheImage.objects.create(file=image_mock, category=1)
        cls.client = APIClient()

    def test_get_blurred_image(self):
        response = self.client.get(f"/api/blurred_images/{self.the_image.pk}/")
        self.assertEqual(response.data['category'], str(1))

    def tearDownModule(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

class FlippedHorizontallyImageViewSetTest(APITestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=(my_media_root))
    def setUp(cls):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        cls.the_image = TheImage.objects.create(file=image_mock, category=3)
        cls.client = APIClient()

    def test_get_flipped_image(self):
        response = self.client.get(f"/api/flipped_horizontally_images/{self.the_image.pk}/")
        self.assertEqual(response.data['category'], str(3))

    def tearDownModule(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

class GrayImageViewSetTest(APITestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=(my_media_root))
    def setUp(cls):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        cls.the_image = TheImage.objects.create(file=image_mock, category=2)
        cls.client = APIClient()

    def test_get_gray_image(self):
        response = self.client.get(f"/api/gray_images/{self.the_image.pk}/")
        self.assertEqual(response.data['category'], str(2))

    def tearDownModule(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass


class SepiaImageViewSetTest(APITestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=(my_media_root))
    def setUp(cls):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        cls.the_image = TheImage.objects.create(file=image_mock, category=4)
        cls.client = APIClient()

    def test_get_sepia_image(self):
        response = self.client.get(f"/api/sepia_images/{self.the_image.pk}/")
        self.assertEqual(response.data['category'], str(4))

    def tearDownModule(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
