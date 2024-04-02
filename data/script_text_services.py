import os


def set_script_file_for_script(script, text_file):
    extension = text_file.filename.split(".")[-1]
    file_path = f"static/text_files/({script.id}) {text_file.filename}.{extension}"
    if os.path.exists(file_path):
        os.remove(file_path)
    text_file.save(file_path)
    script.__setattr__("text_file_path", file_path)
