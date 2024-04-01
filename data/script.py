import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm, ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from data.script_view import script_view


class Script(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'scripts'
    id = Column(Integer,
                primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    small_photo_path = Column(String)
    middle_photo_path = Column(String)
    big_photo_path = Column(String)
    type = Column(String, nullable=False)
    genres = Column(String, nullable=False)

    text_file_path = Column(String, nullable=False)
    text = sqlalchemy.Column(String, nullable=False)

    rating = Column(Float, nullable=False, default=0)

    date_of_publication = Column(DateTime,
                                 default=lambda: datetime.datetime.now().date(), nullable=False)

    user_id = sqlalchemy.Column(Integer, ForeignKey('users.id'))
    author = orm.relationship("User", back_populates='scripts')

    marks = orm.relationship("ScriptMark", back_populates="script")
    marks_count = Column(Integer, nullable=False, default=0)

    reviews = orm.relationship("ScriptReview", back_populates="script")
    reviews_count = Column(Integer, nullable=False, default=0)

    viewed_users = orm.relationship("User", secondary=script_view, back_populates="viewed_scripts")
    views_count = Column(Integer, nullable=False, default=0)

    is_in_users_best_scripts = Column(Boolean, default=False)


