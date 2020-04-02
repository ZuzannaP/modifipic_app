import os

import cv2

from django.http import Http404


def preprocessing_img(new_img_name_prefix, new_folder_name, raw_image):
    """ Converting image to numpy and creating necessary directory paths"""

    # converting image to array in numpy (x*y*3)
    try:
        image = cv2.imread(raw_image.file.path)
    except OSError as e:
        raise Http404("Unable to open image", e)
    except AssertionError as f:
        raise Http404("Unable to open image, upload it again", f)

    dir_path = os.path.dirname(raw_image.file.path)
    img_name = os.path.basename(raw_image.file.name)
    new_img_name = new_img_name_prefix + img_name
    new_dir_path = os.path.join(dir_path, new_folder_name)
    try:
        os.mkdir(new_dir_path)
    except OSError as e:
        if e.errno == 17:  # Directory already exists.
            pass
    return new_img_name, image
