import io
import os

import cv2
import numpy as np

from django.core.files.images import ImageFile
from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework import viewsets

from .models import TheImage
from .serializers import ImageSerializer
from .permissions import GetPostOrAuthenticated

from django.http import JsonResponse
from frontend_modifipic.forms import ImageFileUploadForm


def upload_image_via_form_view(request):
    if request.method == 'POST':
        form = ImageFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'error': False, 'message': 'Image uploaded Successfully'})
        else:
            return JsonResponse({'error': True, 'errors': "Oops! Something went wrong \n" + form.errors})
    else:
        form = ImageFileUploadForm()
        return render(request, 'landing_page.html', {'form': form})


class RawImageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = TheImage.objects.filter(category=0)
    serializer_class = ImageSerializer
    permission_classes = (GetPostOrAuthenticated, )

    # creating directory for modified images, if not already existent
    @staticmethod
    def create_dir(self, path):
        try:
            os.mkdir(path)
        except OSError as e:
            if e.errno == 17:  # Directory already exists.
                pass

    def preprocessing_img(self, new_img_name_prefix, new_folder_name):
        """ Converting image to numpy and creating necessary directory paths"""
        raw_image = self.get_object()

        # converting image to array in numpy (x*y*3)
        try:
            image = cv2.imread(raw_image.file.path)
        except OSError as e:
            raise Http404("Unable to open image", e)
        except AssertionError as f:
            raise Http404("Unable to open image, upload it again", f)

        # todo dodaj messages framework i te errory wypisuj z góry

        dir_path = os.path.dirname(raw_image.file.path)
        img_name = os.path.basename(raw_image.file.name)
        new_img_name = new_img_name_prefix + img_name
        new_dir_path = os.path.join(dir_path, new_folder_name)
        self.create_dir(self, new_dir_path)
        return new_img_name, image

    @action(detail=True, url_path='blur', methods=['get'])
    def blur_image(self, request, *args, **kwargs):
        """ Blurrs the image and saves in database """
        new_img_name_prefix = "blurred_"
        new_folder_name = "blurred"
        new_img_name, image = self.preprocessing_img(new_img_name_prefix, new_folder_name)

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
        new_img_name_prefix = "flipped_hor_"
        new_folder_name = "flipped_horizontally"
        new_img_name, image = self.preprocessing_img(new_img_name_prefix, new_folder_name)

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
        new_img_name_prefix = "gray_"
        new_folder_name = "gray"
        new_img_name, image = self.preprocessing_img(new_img_name_prefix, new_folder_name)

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
        new_img_name_prefix = "sepia_"
        new_folder_name = "sepia"
        new_img_name, image = self.preprocessing_img(new_img_name_prefix, new_folder_name)

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


# #################### PHOTOALBUM

# class AddPhoto(LoginRequiredMixin, View):
#
#     def get(self, request):
#         form = AddPhotoForm()
#         ctx = {"form": form}
#         return render(request, "add_photo_tmp.html", ctx)
#
#     def post(self, request):
#         form = AddPhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             path = form.cleaned_data["path"]
#             description = form.cleaned_data["description"]
#             photo = Photo.objects.create(path=path, owner=request.user, description=description)
#             messages.success(request, 'Photo successfully uploaded')
#             return redirect(f"/photo/{photo.pk}/")
#         ctx = {"form": form}
#         return render(request, "add_photo_tmp.html", ctx)
