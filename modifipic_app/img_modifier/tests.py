import json

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


"""
formularz!!!

serializers
API
"""

class LoginTests(APITestCase):
    @classmethod
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
#
# factory = APIRequestFactory()
# request = factory.post('/notes/', {'title': 'new idea'}, format='json')
'''
from rest_framework.test import force_authenticate

factory = APIRequestFactory()
user = User.objects.get(username='olivia')
view = AccountDetail.as_view()

# Make an authenticated request to the view...
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user)
response = view(request)
'''

