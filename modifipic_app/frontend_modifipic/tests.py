import os

from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from django.urls import reverse

from .forms import ImageFileUploadForm
from img_modifier.models import TheImage

from django.test import override_settings
import shutil


TEST_DIR = 'test_data'
my_media_root = os.path.join(TEST_DIR, 'media')


class ModelTestClass(TestCase):
    @override_settings(MEDIA_ROOT=my_media_root)
    def test_image_upload(self):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        the_image = TheImage.objects.create(file=image_mock)
        self.assertEqual(len(TheImage.objects.all()), 1)
        self.assertTrue(isinstance(the_image, TheImage))

    @classmethod
    def tearDownModule(cls):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass


class ViewTestClass(TestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=my_media_root)
    def setUpTestData(cls):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        cls.the_image = TheImage.objects.create(file=image_mock)

    def test_upload_image_via_form_view_uses_correct_template_and_has_desired_location(self):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')

    def test_modify_image_view_uses_correct_template_and_has_desired_location(self):
        response = self.client.get(reverse('modify', args=(self.the_image.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modify_page.html')

    def test_display_image_view_uses_correct_template_and_has_desired_location(self):
        response = self.client.get(reverse('result', args=(self.the_image.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'result_page.html')

    @classmethod
    def tearDownModule(cls):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass


class FormTestClass(TestCase):
    @override_settings(MEDIA_ROOT=my_media_root)
    def test_form_upload(self):
        with open("img_modifier/tests_data/2.jpg", "rb") as test_photo:
            img = SimpleUploadedFile('image.jpg', content=test_photo.read(), content_type='image/jpg')
        file_data = {'file': img}
        data = {'category': 0}
        form = ImageFileUploadForm(data, file_data)
        self.assertTrue(form.is_valid())
