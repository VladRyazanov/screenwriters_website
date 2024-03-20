import os

from PIL import Image
from werkzeug.utils import secure_filename


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

    new_image.save(output_path, output_path.split(".")[-1].upper())


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


