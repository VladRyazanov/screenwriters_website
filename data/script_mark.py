import datetime

from flask_login import UserMixin
from sqlalchemy import orm, Integer, Column, ForeignKey, DateTime, String
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class ScriptMark(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = "script_marks"
    id = Column(Integer,
                primary_key=True, autoincrement=True)
    mark = Column(Integer)
    date_of_publication = Column(String, default=lambda: str(datetime.datetime.now().date()), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    script_id = Column(Integer, ForeignKey('scripts.id'))

    user = orm.relationship("User", back_populates="given_script_marks")
    script = orm.relationship("Script", back_populates="marks")
