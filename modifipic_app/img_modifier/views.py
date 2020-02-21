import cv2
import numpy as np

from django.core.files import File
from django.http import Http404
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import viewsets

from .models import Image
from .serializers import ImageSerializer


"""
1. Nie umiem naprawić tego, że zapisuje mi dwukrotnie do bazy danych. Chciałąbym usunąć z dysku zdjęcie cv2
 jak już jest zapisane do bazy danych, ale nie wiem jak.
2.Próbowałam wyodrębnić początek każdej z tych funkcji do specjalnej klasy/metody "preprocess_image", ale nie wychodzi.
"""


# nieaktualne , ale trzymaj jako punkt referencyjny

# class ReadImageMixin:
#     model = None
#
#     def get_object(self):
#         raw_image = '/home/zuzanna/Desktop/zdjęcia/kaczki.jpg'
#         image = cv2.imread(raw_image)
#         if image is not None:
#             return image
#         else:
#             raise OSError("Unable to open/read file")


class ImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @action(detail=True, url_path='blur', methods=['get'])
    def blur_image(self, request, *args, **kwargs):
        """ Blurrs the image and saves in database """
        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        image = cv2.imread(raw_image.file.path)
        img_name = raw_image.file.name.split("/")[-1]
        new_img_name = "blurred_" + img_name
        img_path = raw_image.file.path.split(img_name)[0] + new_img_name

        try:
            blurred_img = cv2.GaussianBlur(image, (21, 21), cv2.BORDER_DEFAULT)
            cv2.imwrite(img_path, blurred_img)
            # niepotrzebne, bo poniższe with lepsze, gdyż pozwala na zmianę nazwy zdjęcia
            # Image.objects.create(file=File(open(img_path, "rb")))
            with open(img_path, 'rb') as f:
                data = File(f)
                new_image = Image.objects.create()
                new_image.file.save(new_img_name, data, True)
            return Response("Image has been blurred.")
        except OSError:
            raise Http404("Image not found")

    @action(detail=True, url_path='flip-horizontally', methods=['get'])
    def flip_image_horizontally(self, request, *args, **kwargs):
        """ Flipps the image horizontally """
        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        image = cv2.imread(raw_image.file.path)
        img_name = raw_image.file.name.split("/")[-1]
        new_img_name = "flipped_hor_" + img_name
        img_path = raw_image.file.path.split(img_name)[0] + new_img_name

        try:
            flipped = cv2.flip(image, 1)
            cv2.imwrite(img_path, flipped)
            # Image.objects.create(file=File(open("kaczuszka_flipped.jpg", "rb")))
            with open(img_path, 'rb') as f:
                data = File(f)
                new_image = Image.objects.create()
                new_image.file.save(new_img_name, data, True)
            return Response("Image has been flipped horizontally.")
        except OSError:
            raise Http404("Image not found")

    @action(detail=True, url_path='sepia', methods=['get'])
    def sepia_image(self, request, *args, **kwargs):
        """ Changes image color to sepia """
        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        image = cv2.imread(raw_image.file.path)
        img_name = raw_image.file.name.split("/")[-1]
        new_img_name = "sepia_" + img_name
        img_path = raw_image.file.path.split(img_name)[0] + new_img_name

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
                new_image.file.save(new_img_name, data, True)
            return Response("Image has been desaturated to sepia.")
        except OSError:
            raise Http404("Image not found")

# #######################################################################3
# class ImageViewSet(viewsets.ModelViewSet):
#     """ API endpoint that allows groups to be viewed or edited. """
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#
#
# class BlurView(ReadImageMixin, APIView):
#     """ Blurrs the image """
#     def get(self, request):
#         image = self.get_object()
#         try:
#             blurred_img = cv2.GaussianBlur(image, (21, 21), cv2.BORDER_DEFAULT)
#             cv2.imwrite("kaczuszka_blured.jpg", blurred_img)
#             Image.objects.create(file=File(open("kaczuszka_blured.jpg", "rb")))
#             return Response("Image has been blurred.")
#         except OSError:
#             return "tu wpisz błąd np. http 404 z django.http"
#
#
# class FlipHorizontallyView(ReadImageMixin, APIView):
#     """ Flipps the image horizontally """
#     def get(self, request):
#         image = self.get_object()
#         try:
#             flipped = cv2.flip(image, 1)
#             cv2.imwrite("kaczuszka_flipped.jpg", flipped)
#             Image.objects.create(file=File(open("kaczuszka_flipped.jpg", "rb")))
#             cv2.imwrite("kaczuszka_flipped.jpg", flipped)
#             Image.objects.create(file=File(open("kaczuszka_flipped.jpg", "rb")))
#             return Response("Image has been flipped horizontally.")
#         except OSError:
#             return "tu wpisz błąd np. http 404 z django.http"
#
#
# class SepiaView(ReadImageMixin, APIView):
#     """ Changes image color to sepia """
#     def get(self, request):
#         image = self.get_object()
#         try:
#             img_sepia = cv2.transform(image, np.matrix([[0.272, 0.534, 0.131],
#                                                         [0.349, 0.686, 0.168],
#                                                         [0.393, 0.769, 0.189]
#                                                         ]))
#             # Check which entries have a value greather than 255 and set it to 255
#             img_sepia[np.where(img_sepia > 255)] = 255
#             # Create an image from the array
#             cv2.imwrite("kaczuszka_sepia.jpg", img_sepia)
#             Image.objects.create(file=File(open("kaczuszka_sepia.jpg", "rb")))
#             return Response("Image has been desaturated to sepia.")
#         except OSError:
#             return "tu wpisz błąd np. http 404 z django.http"
