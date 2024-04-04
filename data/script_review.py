import datetime

from flask_login import UserMixin
from sqlalchemy import orm, Integer, Column, ForeignKey, DateTime, String
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class ScriptReview(SqlAlchemyBase, SerializerMixin, UserMixin):
    """
    Класс рецензии на сценарий
    """
    __tablename__ = "script_reviews"
    id = Column(Integer,
                primary_key=True, autoincrement=True)
    # Заголовок и текст рецензии
    title = Column(String)
    text = Column(String)
    date_of_publication = Column(String, default=lambda: str(datetime.datetime.now().date()), nullable=False)
    # Связь с автором рецензии
    user_id = Column(Integer, ForeignKey('users.id'))
    user = orm.relationship("User", back_populates="given_script_reviews")
    # Связь со сценарием
    script_id = Column(Integer, ForeignKey('scripts.id'))
    script = orm.relationship("Script", back_populates="reviews")
