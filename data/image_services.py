import os
import uuid

from PIL import Image
from werkzeug.utils import secure_filename

from constants import *


def change_image_size(image_path, output_path, new_width, new_height):
    width_and_height_ratio = new_width / new_height
    image = Image.open(image_path)
    if image.width / image.height < width_and_height_ratio:
        height = image.width / width_and_height_ratio
        top_and_bottom_difference = (image.height - height) // 2
        image = image.crop((0, top_and_bottom_difference, image.width, top_and_bottom_difference + height))
    else:
        width = image.height * width_and_height_ratio
        right_and_left_difference = (image.width - width) // 2
        image = image.crop((right_and_left_difference, 0, right_and_left_difference + width, image.height))

    new_image = image.resize((new_width, new_height))
    extension = output_path.split(".")[-1]
    new_image.save(output_path, extension)


def save_photo_to_temporary_photos_folder(photo):
    filename = secure_filename(photo.filename)
    path = f"static/images/temporary_photos/{filename}"
    photo.save(path)
    return path


def clear_temporary_photos_folder():
    temporary_photos = os.listdir("static/images/temporary_photos")
    for photo_to_remove in temporary_photos:
        file_path = os.path.join("static/images/temporary_photos", photo_to_remove)
        os.remove(file_path)


def set_photo_for_object(object, photo_path, types_of_photos_and_sizes):
    print(photo_path)
    # подготовка папки для фото
    directory_for_photos_path = f"static/images/{object.__tablename__}/{object.id}"
    if os.path.exists(directory_for_photos_path):
        previous_photos = os.listdir(directory_for_photos_path)
        for photo_to_remove in previous_photos:
            file_path = os.path.join(directory_for_photos_path, photo_to_remove)
            os.remove(file_path)
    else:
        os.makedirs(directory_for_photos_path)

    extension = photo_path.split(".")[-1]
    if extension.lower() == "jpg":
        extension = "jpeg"

    for type_of_photo in types_of_photos_and_sizes:
        unique_id = uuid.uuid4()
        new_path = f"{directory_for_photos_path}/{type_of_photo}_{unique_id}.{extension}"
        print(new_path)
        change_image_size(photo_path, new_path, *types_of_photos_and_sizes[type_of_photo])
        object.__setattr__(f"{type_of_photo}_path", new_path.lstrip("static"))
    clear_temporary_photos_folder()


