import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from data.script_view import script_view


class Script(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'scripts'
    id = Column(Integer,
                primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    photo_path = Column(String, nullable=False)
    type = Column(String, nullable=False)
    genres = Column(String, nullable=False)
    text = sqlalchemy.Column(String, nullable=False)

    rating = Column(Integer, nullable=False, default=0)

    date_of_publication = Column(DateTime,
                                 default=datetime.datetime.now, nullable=False)

    user_id = sqlalchemy.Column(Integer, ForeignKey('users.id'))
    author = orm.relationship("User", back_populates='scripts')

    marks = orm.relationship("ScriptMark", back_populates="script")
    marks_count = Column(Integer, nullable=False, default=0)

    reviews = orm.relationship("ScriptReview", back_populates="script")
    reviews_count = Column(Integer, nullable=False, default=0)

    viewed_users = orm.relationship("User", secondary=script_view, back_populates="viewed_scripts")
    views_count = Column(Integer, nullable=False, default=0)