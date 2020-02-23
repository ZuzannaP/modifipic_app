import os

import cv2
import numpy as np

from django.core.files import File
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework import viewsets

from .models import Image
from .serializers import ImageSerializer
from .permissions import GetPostOrAuthenticated


"""
1. Nie umiem naprawić tego, że zapisuje mi dwukrotnie do bazy danych. Chciałąbym usunąć z dysku zdjęcie cv2
 jak już jest zapisane do bazy danych, ale nie wiem jak.
2.Jak wyodrębnić początek każdej z tych funkcji do specjalnej klasy/metody "preprocess_image"?

        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        try:
            image = cv2.imread(raw_image.file.path)
        except OSError as e:
            raise Http404("Unable to open image", e)

        dir_path = os.path.dirname(raw_image.file.path)
        img_name = os.path.basename(raw_image.file.name)
        new_img_name = "blurred_" + img_name
        new_folder_name = "blurred"
        new_dir_path = os.path.join(dir_path, new_folder_name)
        self.create_dir(self, new_dir_path)
        img_path = os.path.join(new_dir_path, new_img_name)


3. dobrze nazwałam create_dir statyczną metodą?
4. autentykacja
"""


class RawImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Image.objects.filter(category=0)
    serializer_class = ImageSerializer
    permission_classes = (GetPostOrAuthenticated, )

    # creating directory for modified images, if not already existant
    @staticmethod
    def create_dir(self, path):
        try:
            os.mkdir(path)
        except OSError as e:
            if e.errno == 17:  # Directory already exists.
                pass

    @action(detail=True, url_path='blur', methods=['get'])
    def blur_image(self, request, *args, **kwargs):
        """ Blurrs the image and saves in database """
        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        try:
            image = cv2.imread(raw_image.file.path)
        except OSError as e:
            raise Http404("Unable to open image", e)

        dir_path = os.path.dirname(raw_image.file.path)
        img_name = os.path.basename(raw_image.file.name)
        new_img_name = "blurred_" + img_name
        new_folder_name = "blurred"
        new_dir_path = os.path.join(dir_path, new_folder_name)
        self.create_dir(self, new_dir_path)
        img_path = os.path.join(new_dir_path, new_img_name)

        try:
            blurred_img = cv2.GaussianBlur(image, (21, 21), cv2.BORDER_DEFAULT)
            cv2.imwrite(img_path, blurred_img)
            with open(img_path, 'rb') as f:
                data = File(f)
                new_image = Image.objects.create()
                new_image.category = 1
                new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
            return Response("Image has been blurred.")
        except OSError:
            raise Http404("Image not found")

    @action(detail=True, url_path='flip-horizontally', methods=['get'])
    def flip_image_horizontally(self, request, *args, **kwargs):
        """ Flipps the image horizontally """
        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        try:
            image = cv2.imread(raw_image.file.path)
        except OSError as e:
            raise Http404("Unable to open image", e)

        dir_path = os.path.dirname(raw_image.file.path)
        img_name = os.path.basename(raw_image.file.path)
        new_img_name = "flipped_hor_" + img_name
        new_folder_name = "flipped_horizontally"
        new_dir_path = os.path.join(dir_path, new_folder_name)
        self.create_dir(self, new_dir_path)
        img_path = os.path.join(new_dir_path, new_img_name)

        try:
            flipped = cv2.flip(image, 1)
            cv2.imwrite(img_path, flipped)
            with open(img_path, 'rb') as f:
                data = File(f)
                new_image = Image.objects.create()
                new_image.category = 3
                new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
            return Response("Image has been flipped horizontally.")
        except OSError:
            raise Http404("Image not found")

    @action(detail=True, url_path="gray", methods=['get'])
    def gray_image(self, request, *args, **kwargs):
        """ Converts image to black and white """
        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        try:
            image = cv2.imread(raw_image.file.path)
        except OSError as e:
            raise Http404("Unable to open image", e)

        dir_path = os.path.dirname(raw_image.file.path)
        img_name = os.path.basename(raw_image.file.path)
        new_img_name = "gray_" + img_name
        new_folder_name = "gray"
        new_dir_path = os.path.join(dir_path, new_folder_name)
        self.create_dir(self, new_dir_path)
        img_path = os.path.join(new_dir_path, new_img_name)

        try:
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(img_path, grayImage)
            with open(img_path, 'rb') as f:
                data = File(f)
                new_image = Image.objects.create()
                new_image.category = 2
                new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
            return Response("Image has been desaturated to gray.")
        except OSError:
            raise Http404("Image not found")

    @action(detail=True, url_path='sepia', methods=['get'])
    def sepia_image(self, request, *args, **kwargs):
        """ Changes image color to sepia """
        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        try:
            image = cv2.imread(raw_image.file.path)
        except OSError as e:
            raise Http404("Unable to open image", e)

        dir_path = os.path.dirname(raw_image.file.path)
        img_name = os.path.basename(raw_image.file.path)
        new_img_name = "sepia_" + img_name
        new_folder_name = "sepia"
        new_dir_path = os.path.join(dir_path, new_folder_name)
        self.create_dir(self, new_dir_path)
        img_path = os.path.join(new_dir_path, new_img_name)

        try:
            img_sepia = cv2.transform(image, np.matrix([[0.272, 0.534, 0.131],
                                                        [0.349, 0.686, 0.168],
                                                        [0.393, 0.769, 0.189]
                                                        ]))

            # Check which entries have a value greather than 255 and set it to 255
            img_sepia[np.where(img_sepia > 255)] = 255

            # Create an image from the array
            cv2.imwrite(img_path, img_sepia)
            with open(img_path, 'rb') as f:
                data = File(f)
                new_image = Image.objects.create()
                new_image.category = 4
                new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
            return Response("Image has been desaturated to sepia.")
        except OSError:
            raise Http404("Image not found")


class BluredImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Image.objects.filter(category=1)
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FlippedHorizontallyImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Image.objects.filter(category=3)
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GrayImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Image.objects.filter(category=2)
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SepiaImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Image.objects.filter(category=4)
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

