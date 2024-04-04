from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField, \
    SelectField
from wtforms.validators import DataRequired

from constants import *

"""
Файл для форм, связанных со сценариями
"""


class CreateScriptForm(FlaskForm):
    """
    Форма для создания сценария
    """
    title = StringField('Название', validators=[DataRequired()])
    type = SelectField('Тип', choices=[(i, i) for i in TYPES_OF_SCRIPTS], validators=[DataRequired()])
    genre = SelectField("Жанр", choices=[(i, i) for i in GENRES], validators=[DataRequired()])
    extra_genre = SelectField("Второй жанр (при необходимости)",
                              choices=[("", "Без второго жанра")] + [(i, i) for i in GENRES])
    description = TextAreaField("Описание", validators=[DataRequired()])
    photo = FileField('Изображение', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif']), DataRequired()])
    text_file = FileField('Текст в формате docx или pdf',
                          validators=[FileAllowed(['docx', 'pdf', 'doc']), DataRequired()])
    submit = SubmitField('Опубликовать')


class EditScriptForm(CreateScriptForm):
    """
    Форма для редактирования сценария
    """
    # Обязательные поля с фотографией и текстом заменены на необязательные,
    # которые используются только для замены фото и текста соответственно
    photo = FileField('Новое изображение (при необходимости)', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    text_file = FileField('Новый текст (при необходимости)', validators=[FileAllowed(['docx', 'pdf', 'doc'])])


class AddScriptReviewForm(FlaskForm):
    """
    Форма для добавления рецензии
    """
    title = StringField('Название', validators=[DataRequired()])
    text = TextAreaField('Текст рецензии', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')


class AddScriptMarkForm(FlaskForm):
    """
    Форма для добавления оценки
    """
    mark = SelectField("Оценка", choices=[(i, i) for i in range(1, 11)], validators=[DataRequired()])
    submit = SubmitField('Оценить')
