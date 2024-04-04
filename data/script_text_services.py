import os


"""
Файл для работы с текстом сценария, служит для присваивания текстового файла сценарию 
"""


def set_script_file_for_script(script, text_file):
    # Присваивание текстового файла сценарию
    text_files_folder_path = "static/text_files"
    if not os.path.exists(text_files_folder_path):
        os.makedirs(text_files_folder_path)
    # Если папка для текста этого сценария уже есть, то удаляем предыдущий сценарий, иначе - создаем эту папку
    this_script_folder_path = f"{text_files_folder_path}/{script.id}"
    if os.path.exists(this_script_folder_path):
        previous_texts = os.listdir(this_script_folder_path)
        for text_to_remove in previous_texts:
            file_path = os.path.join(this_script_folder_path, text_to_remove)
            os.remove(file_path)
    else:
        os.makedirs(this_script_folder_path)

    # Сохраняем файл и присваиваем сценарию
    file_path = f"{this_script_folder_path}/{text_file.filename}"
    text_file.save(file_path)
    script.__setattr__("text_file_path", file_path)
