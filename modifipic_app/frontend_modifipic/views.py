import io
import os

import cv2
import numpy as np

from django.core.files.images import ImageFile
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from .forms import ImageFileUploadForm
from img_modifier.models import TheImage


def upload_image_via_form_view(request):
    if request.method == 'POST':
        form = ImageFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            image = TheImage.objects.create(file=file)
            return redirect(f"modify/{image.pk}")
        else:
            # todo insert here message
            return "Something went wrong"
    else:
        form = ImageFileUploadForm()
        return render(request, 'landing_page.html', {'form': form})


class ModifyImageView(View):
    def get(self, request, pk):
        return render(request, 'modify_page.html')

    def post(self, request, pk):

        def create_dir(path):
            try:
                os.mkdir(path)
            except OSError as e:
                if e.errno == 17:  # Directory already exists.
                    pass

        def preprocessing_img(new_img_name_prefix, new_folder_name):
            """ Converting image to numpy and creating necessary directory paths"""

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
            create_dir(new_dir_path)
            return new_img_name, image

        chosen_modification = request.POST.get("modificationType")
        raw_image = TheImage.objects.get(pk=pk)

        if chosen_modification == "blurred":
            new_img_name_prefix = "blurred_"
            new_folder_name = "blurred"
            new_img_name, image = preprocessing_img(new_img_name_prefix, new_folder_name)

            try:
                blurred_img = cv2.GaussianBlur(image, (21, 21), cv2.BORDER_DEFAULT)

                # creates object comparable to temporary file in RAM
                is_success, buffer = cv2.imencode(".jpg", blurred_img)
                io_buf = io.BytesIO(buffer)
                data = ImageFile(io_buf)
                new_image = TheImage()
                new_image.category = 1
                new_image.file.save(os.path.join(new_folder_name, new_img_name), data)
                return redirect(f"/result/{new_image.pk}")
            except OSError:
                raise Http404("Image not found")

        elif chosen_modification == "sepia":
            new_img_name_prefix = "sepia_"
            new_folder_name = "sepia"
            new_img_name, image = preprocessing_img(new_img_name_prefix, new_folder_name)

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
                return redirect(f"/result/{new_image.pk}")
            except OSError:
                raise Http404("Image not found")

        elif chosen_modification == "gray":
            new_img_name_prefix = "gray_"
            new_folder_name = "gray"
            new_img_name, image = preprocessing_img(new_img_name_prefix, new_folder_name)

            try:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # creates object comparable to temporary file in RAM
                is_success, buffer = cv2.imencode(".jpg", gray_image)
                io_buf = io.BytesIO(buffer)
                data = ImageFile(io_buf)
                new_image = TheImage()
                new_image.category = 2
                new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
                return redirect(f"/result/{new_image.pk}")
            except OSError:
                raise Http404("Image not found")

        elif chosen_modification == "flipped-horizontally":
            new_img_name_prefix = "flipped_hor_"
            new_folder_name = "flipped_horizontally"
            new_img_name, image = preprocessing_img(new_img_name_prefix, new_folder_name)

            try:
                flipped = cv2.flip(image, 1)
                # creates object comparable to temporary file in RAM
                is_success, buffer = cv2.imencode(".jpg", flipped)
                io_buf = io.BytesIO(buffer)
                data = ImageFile(io_buf)
                new_image = TheImage()
                new_image.category = 3
                new_image.file.save(os.path.join(new_folder_name, new_img_name), data, True)
                return redirect(f"/result/{new_image.pk}")
            except OSError:
                raise Http404("Image not found")


def display_image_view(request, pk):
    if request.method == 'GET':
        image = TheImage.objects.get(pk=pk)
        ctx = {'image': image}
        return render(request, 'result_page.html', ctx)
