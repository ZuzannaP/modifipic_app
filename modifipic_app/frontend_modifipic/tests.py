from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .forms import ImageFileUploadForm
from img_modifier.models import TheImage


class ModelTestClass(TestCase):
    def test_image_upload(self):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        the_image = TheImage.objects.create(file=image_mock)
        self.assertEqual(len(TheImage.objects.all()), 1)
        self.assertTrue(isinstance(the_image, TheImage))


class ViewTestClass(TestCase):
    @classmethod
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


# FORM TEST CLASS NOT WORKING

# class FormTestClass(TestCase):
#     def test_form_upload(self):
#         img = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
#         data = {'file': 'img'}
#         form = ImageFileUploadForm(data=data)
#         print(form.errors)
#         #error mówi, że pole file jest required
#         self.assertTrue(form.is_valid())

    #     other attempts
    #
    # def get_temporary_image(self, temp_file):
    #     size = (200, 200)
    #     image = Image.new("RGB", size)
    #     image.save(temp_file, 'jpeg')
    #     return temp_file
    #
    # @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory().name)
    # def test_form_upload(self):
    #     temp_file = tempfile.NamedTemporaryFile()
    #     test_image = self.get_temporary_image(temp_file)
    #
    #     # image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    #     # print(type(image))
    #     # image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
    #
    #     data = {'file':test_image.name, "category":0, }
    #     form = ImageFileUploadForm(data=data)
    #     print(form.errors)
    #     self.assertTrue(form.is_valid())



