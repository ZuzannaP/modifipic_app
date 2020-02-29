import tempfile

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

import mock
from django.core.files import File
from rest_framework import status, response

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from .models import TheImage
from .serializers import ImageSerializer
from frontend_modifipic.forms import ImageFileUploadForm

"""
serializers
permissions
API
"""


class ModelTestClass(TestCase):
    def test_image_upload(self):
        image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        the_image = TheImage.objects.create(file=image_mock)
        self.assertEqual(len(TheImage.objects.all()), 1)
        self.assertTrue(isinstance(the_image, TheImage))


class FormTestClass(TestCase):
    def test_form_upload(self):
        img = "SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')"
        data = {'file': img}
        form = ImageFileUploadForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())

        # other attempts

#     def get_temporary_image(self, temp_file):
#         size = (200, 200)
#         image = Image.new("RGB", size)
#         image.save(temp_file, 'jpeg')
#         return temp_file
#
#     @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory().name)
#     def test_form_upload(self):
#         temp_file = tempfile.NamedTemporaryFile()
#         test_image = self.get_temporary_image(temp_file)
#
#         # image = tempfile.NamedTemporaryFile(suffix=".jpg").name
#         # print(type(image))
#         # image_mock = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
#
#         data = {'file':test_image.name, "category":0, }
#         form = ImageFileUploadForm(data=data)
#         print(form.errors)
#         self.assertTrue(form.is_valid())
    #





    #
    # def test_valid_choose_meeting_location_form(self):
    #     self.e.meeting_address = "Nice Street"
    #     self.e.meeting_geographical_coordinates = "Point(13 13)"
    #     self.e.location_comments = "The key is under doormat"
    #     data = {'meeting_address': self.e.meeting_address,
    #             "meeting_geographical_coordinates": self.e.meeting_geographical_coordinates,
    #             "location_comments": self.e.location_comments}
    #     form = ChooseMeetingLocationForm(data=data)
    #     self.assertTrue(form.is_valid())
    #
    # def test_invalid_choose_meeting_location_form(self):
    #     """omitting "meeting_geographical_coordinates" on purpose"""
    #     self.e.meeting_address = "Big Street"
    #     self.e.meeting_geographical_coordinates = "Point(13 13)"
    #     self.e.location_comments = "The key is vase"
    #     data = {'meeting_address': self.e.meeting_address,
    #             "meeting_geographical_coordinates": "",
    #             "location_comments": self.e.location_comments}
    #     form = ChooseMeetingLocationForm(data=data)
    #     self.assertFalse(form.is_valid())
    #
    # def test_valid_edit_event_form(self):
    #     self.test_participant = CustomUser.objects.create_user(first_name="PanPat", last_name="Participant",
    #                                                            username="pan_participant",
    #                                                            password="pan_participantpan_participant",
    #                                                            email="participant@wp.pl",
    #                                                            geographical_coordinates="Point(14 14)")
    #     self.e.participants.add(self.test_participant)
    #     form = EditEventForm(excluding_owner=self.c)
    #     displayed_participants = form.fields['participants'].queryset.all()
    #     self.assertTrue(self.c not in displayed_participants)
    #
    # def test_valid_edit_meeting_location_form(self):
    #     self.e.meeting_address = "Big Street"
    #     self.e.meeting_geographical_coordinates = "Point(4 4)"
    #     self.e.location_comments = "There are no doors. Use window"
    #     data = {'meeting_address': self.e.meeting_address,
    #             "meeting_geographical_coordinates": self.e.meeting_geographical_coordinates,
    #             "location_comments": self.e.location_comments}
    #     form = ImageFileUploadForm(data=data)
    #     self.assertTrue(form.is_valid())
    #
    # def test_invalid_edit_meeting_location_form(self):
    #     """omitting "meeting_address" on purpose"""
    #     self.e.meeting_address = "Big Street"
    #     self.e.meeting_geographical_coordinates = "Point(4 4)"
    #     self.e.location_comments = "There are no doors. Use window"
    #     data = {'meeting_address': "",
    #             "meeting_geographical_coordinates": self.e.meeting_geographical_coordinates,
    #             "location_comments": self.e.location_comments}
    #     form = ImageFileUploadForm(data=data)
    #     self.assertFalse(form.is_valid())


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



# other app tests
'''
from django.test import TestCase
from django.test import Client
from django.urls import reverse



class ViewsUserTestClass(TestCase):
    def setUp(self):
        self.test_user = CustomUser.objects.create_user(first_name="Pan", last_name="Tester", username="pan_tester",
                                                        password="pantesterpantester", email="pan@wp.pl",
                                                        geographical_coordinates="Point(12 12)")

    def test_login(self):
        c = Client()
        response = c.login(username="pan_tester", password="pantesterpantester")
        self.assertTrue(response)

    def test_access_for_logged_in(self):
        c = Client()
        c.login(username="pan_tester", password="pantesterpantester")
        response = c.get(reverse("guest_in_progress"))
        self.assertEqual(response.status_code, 200)

    def test_restrictions_for_logged_out(self):
        """ logged-out user can not access urls restricted for logged-in users """
        c = Client()
        c.logout()
        response = c.get(reverse("guest_in_progress"))
        self.assertRedirects(response, "/login/?next=/event/guest/in_progress/")


class ViewsAppLogicTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUser.objects.create_user(first_name="Pan", last_name="Tester", username="pan_tester",
                                                       password="pantesterpantester", email="pan@wp.pl",
                                                       geographical_coordinates="Point(12 12)")
        cls.test_participant = CustomUser.objects.create_user(first_name="Pan2", last_name="Tester2",
                                                              username="pan_tester2", password="pantester2pantester2",
                                                              email="pan2@wp.pl",
                                                              geographical_coordinates="Point(12 12)")
        cls.test_event = Event.objects.create(title="My event", description="Great event", owner=cls.test_user)
        cls.test_event.participants.add(cls.test_participant)
        cls.test_datetimeslot = DateTimeSlot.objects.create(date_time_from="2021-03-18 17:30:00+01",
                                                            date_time_to="2021-03-18 20:00:00+01",
                                                            event=cls.test_event)
        cls.test_participantslotvote = ParticipantSlotVote.objects.create(participant=cls.test_participant,
                                                                          slot=cls.test_datetimeslot, vote=1)
        cls.client = Client()

    def test_create_event_view_uses_correct_template_and_has_desired_location(self):
        self.client.login(username="pan_tester", password="pantesterpantester")
        response = self.client.get(reverse('create_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_event_tmp.html')

    def test_choose_meeting_location_view_uses_correct_template_and_has_desired_location(self):
        self.client.login(username="pan_tester", password="pantesterpantester")
        response = self.client.get(reverse('choose_location', args=(self.test_event.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choose_meeting_location_tmp.html')

  

'''
