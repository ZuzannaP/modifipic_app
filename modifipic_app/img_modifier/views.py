import cv2
import numpy as np
from django.core.files import File

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


from .models import Image
from .serializers import ImageSerializer


# class that converts image to array in numpy (x*y*3)
from modifipic_app.settings import MEDIA_URL


class ReadImageMixin:
    model = None

    def get_object(self):
        # raw_image = Image.objects.get(pk=pk)
        raw_image = '/home/zuzanna/Desktop/zdjęcia/kaczki.jpg'
        image = cv2.imread(raw_image)
        if image is not None:
            return image
        else:
            raise OSError("Unable to open/read file")


class ImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class BlurView(ReadImageMixin, APIView):
    """ Blurrs the image """
    def get(self, request):
        image = self.get_object()
        try:
            blurred_img = cv2.GaussianBlur(image, (21, 21), cv2.BORDER_DEFAULT)
            cv2.imwrite("kaczuszka_blured.jpg", blurred_img)
            Image.objects.create(file=File(open("kaczuszka_blured.jpg", "rb")))
            return Response("Image has been blurred.")
        except OSError:
            return "tu wpisz błąd np. http 404 z django.http"


class FlipHorizontallyView(ReadImageMixin, APIView):
    """ Flipps the image horizontally """
    def get(self, request):
        image = self.get_object()
        try:
            flipped = cv2.flip(image, 1)
            cv2.imwrite("kaczuszka_flipped.jpg", flipped)
            Image.objects.create(file=File(open("kaczuszka_flipped.jpg", "rb")))
            cv2.imwrite("kaczuszka_flipped.jpg", flipped)
            Image.objects.create(file=File(open("kaczuszka_flipped.jpg", "rb")))
            return Response("Image has been flipped horizontally.")
        except OSError:
            return "tu wpisz błąd np. http 404 z django.http"


class SepiaView(ReadImageMixin, APIView):
    """ Changes image color to sepia """
    def get(self, request):
        image = self.get_object()
        try:
            img_sepia = cv2.transform(image, np.matrix([[0.272, 0.534, 0.131],
                                                        [0.349, 0.686, 0.168],
                                                        [0.393, 0.769, 0.189]
                                                        ]))
            # Check which entries have a value greather than 255 and set it to 255
            img_sepia[np.where(img_sepia > 255)] = 255
            # Create an image from the array
            cv2.imwrite("kaczuszka_sepia.jpg", img_sepia)
            Image.objects.create(file=File(open("kaczuszka_sepia.jpg", "rb")))
            return Response("Image has been desaturated to sepia.")
        except OSError:
            return "tu wpisz błąd np. http 404 z django.http"



