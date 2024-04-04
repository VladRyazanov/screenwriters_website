import datetime

from flask_login import UserMixin
from sqlalchemy import orm, Integer, String, Column, DateTime
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase
from data.script_view import script_view
from data.subscription import subscription


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """
    Класс пользователя
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # Пути для фотографий разного размера
    small_photo_path = Column(String)
    middle_photo_path = Column(String)
    big_photo_path = Column(String)

    social_networks = Column(String, nullable=True)
    modified_date = Column(String, default=lambda: str(datetime.datetime.now().date()), nullable=False)
    rating = Column(Integer, default=0)

    # Связь с таблицей оценок
    given_script_marks = orm.relationship("ScriptMark", back_populates="user")
    # Связь с таблицей рецензий
    given_script_reviews = orm.relationship("ScriptReview", back_populates="user")
    # Связь с таблицей сценариев
    scripts = orm.relationship("Script", back_populates='author')
    # Связь с отношением многих ко многим для подписок
    subscriptions = orm.relationship('User',
                                     secondary=subscription,
                                     primaryjoin=(id == subscription.c.subscriber_id),
                                     secondaryjoin=(id == subscription.c.subscribed_to_id),
                                     backref='subscribers')
    # Количество подписчиков
    subscribers_count = Column(Integer, default=0)
    # Связь с отношением многих ко многим для просмотров сценариев
    viewed_scripts = orm.relationship("Script",
                                      secondary=script_view, back_populates="viewed_users")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
