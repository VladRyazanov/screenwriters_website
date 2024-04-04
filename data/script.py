import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm, ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from data.script_view import script_view


class Script(SqlAlchemyBase, SerializerMixin, UserMixin):
    """
    Класс сценария
    """
    __tablename__ = 'scripts'
    id = Column(Integer,
                primary_key=True, autoincrement=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    # Пути к различным фотографиям (большое - для страницы этого сценария,
    # среднее - для отображения на главной странице, маленькое - для отображения на странице пользователя)
    small_photo_path = Column(String)
    middle_photo_path = Column(String)
    big_photo_path = Column(String)
    # Тип (полнометражный/короткометражный фильм, сериал)
    type = Column(String, nullable=False)
    # Жанры
    genres = Column(String, nullable=False)
    # путь к текстовому файлу
    text_file_path = Column(String, nullable=False)
    rating = Column(Float, nullable=False, default=0)

    date_of_publication = Column(String, default=lambda: str(datetime.datetime.now().date()), nullable=False)
    # Связь с таблицей пользователей
    user_id = sqlalchemy.Column(Integer, ForeignKey('users.id'))
    author = orm.relationship("User", back_populates='scripts')
    # Связь с таблицей оценок
    marks = orm.relationship("ScriptMark", back_populates="script")
    marks_count = Column(Integer, nullable=False, default=0)
    # Связь с таблицей рецензий
    reviews = orm.relationship("ScriptReview", back_populates="script")
    reviews_count = Column(Integer, nullable=False, default=0)
    # Связь с таблицей пользователей для просмотров сценариев (с отношением многих ко многим)
    viewed_users = orm.relationship("User", secondary=script_view, back_populates="viewed_scripts")
    views_count = Column(Integer, nullable=False, default=0)



