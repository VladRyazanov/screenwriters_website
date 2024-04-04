import os
import uuid

from PIL import Image
from werkzeug.utils import secure_filename


"""
Файл для работы с изображениями, служит для изменения размера изображения,
 временного сохранения изображения и установки изображения для различных объектов
"""


def change_image_size(image_path, output_path, new_width, new_height):
    # Функция для изменения размера и соотношения сторон изображения
    # Находим соотношение ширины и высоты, которого требуется достигнуть
    width_and_height_ratio = new_width / new_height
    image = Image.open(image_path)
    # Если соотношение сторон изображения меньше, чем требуется (высота слишком большая)
    if image.width / image.height < width_and_height_ratio:
        # находим высоту, которая будет соответствовать текущей ширине изображения по соотношению сторон
        # (ширина оставлена исходной, т.к. это позволит сохранить максимальное разрешение изображения)
        height = image.width / width_and_height_ratio
        # считаем разницу между исходной высотой и требующейся и делим на 2 (изображение будет обрезано до нужного
        # размера, вырезается именно центральная часть)
        top_and_bottom_difference = (image.height - height) // 2
        # Обрезаем изображение и получаем новое, с нужным соотношением сторон
        image = image.crop((0, top_and_bottom_difference, image.width, top_and_bottom_difference + height))
    else:
        # Если же соотношение ширины и высоты больше, чем требуется (изображение слишком широкое)
        # Находим ширину, которая соответствует высоте изображения
        width = image.height * width_and_height_ratio
        # Обрезаем, оставляя центральную часть с нужным соотношением сторон
        right_and_left_difference = (image.width - width) // 2
        image = image.crop((right_and_left_difference, 0, right_and_left_difference + width, image.height))

    # Изменяем размер получившегося изображения до требующегося
    # (соотношение сторон изменено на нужное, и изображение не будет непропорционально сжато или растянуто)
    new_image = image.resize((new_width, new_height))
    # Сохранение
    extension = output_path.split(".")[-1]
    new_image.save(output_path, extension)


def save_photo_to_temporary_photos_folder(photo):
    # Сохранение фото в папку временных фотографий
    # Нужно для того, чтобы сразу после загрузки на сайт изображения на время сохранить его,
    # а потом изменить размер и присвоить объектам
    filename = secure_filename(photo.filename)
    static_folder_path = "static/images/temporary_photos"
    if not os.path.exists(static_folder_path):
        os.makedirs(static_folder_path)
    path = f"{static_folder_path}/{filename}"
    photo.save(path)
    return path


def clear_temporary_photos_folder():
    # Очистка папки временных фотографий
    temporary_photos = os.listdir("static/images/temporary_photos")
    for photo_to_remove in temporary_photos:
        file_path = os.path.join("static/images/temporary_photos", photo_to_remove)
        os.remove(file_path)


def set_photo_for_object(object, photo_path, types_of_photos_and_sizes):
    # Функция для установки фотографий объектам (например, для установки фото у пользователя)
    # подготовка папки для фото
    # Создаем папку с фотографиями объектов этого класса (Например, с фото пользователей или сценариев)
    if not os.path.exists(f"static/images/{object.__tablename__}"):
        os.makedirs(f"static/images/{object.__tablename__}")
    # Путь к папке с фото этого объекта
    directory_for_photos_path = f"static/images/{object.__tablename__}/{object.id}"
    # Если такой объект уже есть, удаляем все его предыдущие фото, если нет - создаем для него папку
    if os.path.exists(directory_for_photos_path):
        previous_photos = os.listdir(directory_for_photos_path)
        for photo_to_remove in previous_photos:
            file_path = os.path.join(directory_for_photos_path, photo_to_remove)
            os.remove(file_path)
    else:
        os.makedirs(directory_for_photos_path)

    extension = photo_path.split(".")[-1]
    # Библиотека PIL плохо работает с jpg, поэтому, при необходимости, исправляем расширение фото
    if extension.lower() == "jpg":
        extension = "jpeg"

    # Для каждого типа фотографий (например, большое фото для страницы пользователя,
    # маленькое - для отображения в карточке сценария) создаем новое изображение и сохраняем в папку
    for type_of_photo in types_of_photos_and_sizes:
        new_path = f"{directory_for_photos_path}/{type_of_photo}.{extension}"
        change_image_size(photo_path, new_path, *types_of_photos_and_sizes[type_of_photo])
        object.__setattr__(f"{type_of_photo}_path", new_path.lstrip("static"))
    # Очищаем папку временных фото, т.к. фото уже установлены
    clear_temporary_photos_folder()
