import datetime

from flask_login import UserMixin
from sqlalchemy import orm, Integer, Column, ForeignKey, DateTime, String
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class ScriptMark(SqlAlchemyBase, SerializerMixin, UserMixin):
    """
    Класс оценки сценария
    """
    __tablename__ = "script_marks"
    id = Column(Integer,
                primary_key=True, autoincrement=True)
    # Оценка (от 1 до 10)
    mark = Column(Integer)
    date_of_publication = Column(String, default=lambda: str(datetime.datetime.now().date()), nullable=False)
    # Связь с оценившим пользователем
    user_id = Column(Integer, ForeignKey('users.id'))
    user = orm.relationship("User", back_populates="given_script_marks")
    # Связь с оценённым сценарием
    script_id = Column(Integer, ForeignKey('scripts.id'))
    script = orm.relationship("Script", back_populates="marks")
