from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    photo = FileField('Фото пользователя', validators=[FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    description = TextAreaField("Немного о себе", validators=[DataRequired()])

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

    submit = SubmitField('Войти')


class EditUserForm(FlaskForm):
    photo = FileField('Изменить фото', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    description = TextAreaField("Немного о себе", validators=[DataRequired()])

    submit = SubmitField('Готово')





