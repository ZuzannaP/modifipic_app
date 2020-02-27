import io
import os

import cv2
import numpy as np

from django.core.files.images import ImageFile
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework import viewsets

from .models import TheImage
from .serializers import ImageSerializer
from .permissions import GetPostOrAuthenticated

from modifipic_app import utils


class RawImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = TheImage.objects.filter(category=0)
    serializer_class = ImageSerializer
    permission_classes = (GetPostOrAuthenticated, )

    @action(detail=True, url_path='blur', methods=['get'])
    def blur_image(self, request, *args, **kwargs):
        """ Blurrs the image and saves in database """
        raw_image = self.get_object()
        new_img_name_prefix = "blurred_"
        new_folder_name = "blurred"
        new_img_name, image = utils.preprocessing_img(new_img_name_prefix, new_folder_name, raw_image)

        try:
            blurred_img = cv2.GaussianBlur(image, (21, 21), cv2.BORDER_DEFAULT)

            # creates object comparable to temporary file in RAM
            is_success, buffer = cv2.imencode(".jpg", blurred_img)
            io_buf = io.BytesIO(buffer)
            data = ImageFile(io_buf)
            new_image = TheImage()
            new_image.category = 1
            new_image.file.save(os.path.join(new_folder_name, new_img_name), data)
            return Response("Image has been blurred.")
        except OSError:
            raise Http404("Image not found")

    @action(detail=True, url_path='flip-horizontally', methods=['get'])
    def flip_image_horizontally(self, request, *args, **kwargs):
        """ Flipps the image horizontally """
        raw_image = self.get_object()
        new_img_name_prefix = "flipped_hor_"
        new_folder_name = "flipped_horizontally"
        new_img_name, image = utils.preprocessing_img(new_img_name_prefix, new_folder_name, raw_image)

        try:
            flipped = cv2.flip(image, 1)
            # creates object comparable to temporary file in RAM
            is_success, buffer = cv2.imencode(".jpg", flipped)
            io_buf = io.BytesIO(buffer)
            data = ImageFile(io_buf)
            new_image = TheImage()
            new_image.category = 3
            new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
            return Response("Image has been flipped horizontally.")
        except OSError:
            raise Http404("Image not found")

    @action(detail=True, url_path="gray", methods=['get'])
    def gray_image(self, request, *args, **kwargs):
        """ Converts image to black and white """
        raw_image = self.get_object()
        new_img_name_prefix = "gray_"
        new_folder_name = "gray"
        new_img_name, image = utils.preprocessing_img(new_img_name_prefix, new_folder_name, raw_image)

        try:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # creates object comparable to temporary file in RAM
            is_success, buffer = cv2.imencode(".jpg", gray_image)
            io_buf = io.BytesIO(buffer)
            data = ImageFile(io_buf)
            new_image = TheImage()
            new_image.category = 2
            new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
            return Response("Image has been desaturated to gray.")
        except OSError:
            raise Http404("Image not found")

    @action(detail=True, url_path='sepia', methods=['get'])
    def sepia_image(self, request, *args, **kwargs):
        """ Changes image color to sepia """
        raw_image = self.get_object()
        new_img_name_prefix = "sepia_"
        new_folder_name = "sepia"
        new_img_name, image = utils.preprocessing_img(new_img_name_prefix, new_folder_name, raw_image)

        try:
            img_sepia = cv2.transform(image, np.matrix([[0.272, 0.534, 0.131],
                                                        [0.349, 0.686, 0.168],
                                                        [0.393, 0.769, 0.189]
                                                        ]))

            # Check which entries have a value greater than 255 and set it to 255
            img_sepia[np.where(img_sepia > 255)] = 255

            # creates object comparable to temporary file in RAM
            is_success, buffer = cv2.imencode(".jpg", img_sepia)
            io_buf = io.BytesIO(buffer)
            data = ImageFile(io_buf)
            new_image = TheImage()
            new_image.category = 4
            new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
            return Response("Image has been desaturated to sepia.")
        except OSError:
            raise Http404("Image not found")


class BluredImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = TheImage.objects.filter(category=1)
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FlippedHorizontallyImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = TheImage.objects.filter(category=3)
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GrayImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = TheImage.objects.filter(category=2)
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SepiaImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = TheImage.objects.filter(category=4)
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
