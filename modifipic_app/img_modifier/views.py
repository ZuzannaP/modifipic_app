from django.shortcuts import render
import cv2
import numpy as np

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Image

'''
1. czemu ReadImageMixin nie zwraca ładnie obiektu 'image' do 'BlurView'
2. Czemu po wejściu na serwer nie widzę łądnie Django Rest Framework tylko error, ze nie ma takiej ścieżki i muszę
 ręcznie blur wpisać, żeby przeniosło mnie na resta
3. Jak sensownie zrobić taki image flow?
    zapisać w bazie tylko skończone zdjęcie, a pierwone tylko w locie obrobić?
    jak to wszystko zrobić? 
4. Nie umiem tego obiektu cv2.imwrite do zmiennej zapisać, by potem zapisać zdjęcie w bazie django (jak przypisuję
    standardowo zmienną to robi się boolean
'''
# class that converts image to array in numpy (x*y*3)
class ReadImageMixin(object):
    model = None

    def get_object(self):
        # raw_image = Image.objects.get(pk=pk)
        raw_image = '/home/zuzanna/Desktop/zdjęcia/kaczki.jpg'
        image = cv2.imread(raw_image)
        if image:
            return image
        else:
            raise OSError("Unable to open/read file")


class BlurView(ReadImageMixin, APIView):
    def get(self, request, image):
        # raw_image = '/home/zuzanna/Desktop/zdjęcia/kaczki.jpg'
        # image = cv2.imread(raw_image)
        if image is not None:
            blurred_img = cv2.GaussianBlur(image, (21, 21), cv2.BORDER_DEFAULT)
            cv2.imwrite("img_modifier/media/kaczuszka.jpg", blurred_img)
            # print(my_blurred_img)
            # Image.objects.create(file=my_blurred_img)
            return Response("yeas")
        else:
            return Response(None)

#
# def flip_horizontally(image):
#     flipped = cv2.flip(image, 1)
#     return flipped
#
#
# def sepia(image):
#     sepia_me = cv2.transform(image, np.matrix([[0.272, 0.534, 0.131],
#                                                [0.349, 0.686, 0.168],
#                                               [0.393, 0.769, 0.189]
#                                                ]))
#
#     # Check which entries have a value greather than 255 and set it to 255
#     sepia_me[np.where(sepia_me > 255)] = 255
#
#     # Create an image from the array
#     return sepia_me



# kurcze = '/home/zuzanna/Desktop/zdjęcia/kaczki.jpg'
# kurcze_img = read_image(kurcze)

# kurcze_img = '/home/zuzanna/Desktop/zdjęcia/kaczki.jpg'


# flipped_kurcze = flip_horizontally(kurcze_img)
# sepia_kurcze = sepia(kurcze_img)
#
# cv2.imshow('kurcze', kurcze_img)
# cv2.imshow('flipped_kurcze', flipped_kurcze)
# cv2.imshow('sepia_kurcze', sepia_kurcze)
#
#
#
# cv2.waitKey(0)
