import datetime

from flask_login import UserMixin
from sqlalchemy import orm, Integer, Column, ForeignKey, DateTime, String
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class ScriptReview(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = "script_reviews"
    id = Column(Integer,
                primary_key=True, autoincrement=True)

    title = Column(String)
    text = Column(String)
    date_of_publication = Column(String, default=lambda: str(datetime.datetime.now().date()), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    script_id = Column(Integer, ForeignKey('scripts.id'))

    user = orm.relationship("User", back_populates="given_script_reviews")
    script = orm.relationship("Script", back_populates="reviews")
