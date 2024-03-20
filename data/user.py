import datetime
import os

from flask_login import UserMixin
from sqlalchemy import orm, Integer, String, Column, DateTime
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from data.db_session import SqlAlchemyBase
from data.subscription import subscription
from data.script_view import script_view
from data.image_services import change_image_size


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    small_photo_path = Column(String)
    middle_photo_path = Column(String)
    big_photo_path = Column(String)

    social_networks = Column(String, nullable=True)
    modified_date = Column(DateTime, default=datetime.datetime.now)
    rating = Column(Integer, default=0)

    given_script_marks = orm.relationship("ScriptMark", back_populates="user")
    given_script_reviews = orm.relationship("ScriptReview", back_populates="user")
    scripts = orm.relationship("Script", back_populates='author')
    subscriptions = orm.relationship('User',
                                     secondary=subscription,
                                     primaryjoin=(id == subscription.c.subscriber_id),
                                     secondaryjoin=(id == subscription.c.subscribed_to_id),
                                     backref='subscribers')
    subscribers_count = Column(Integer, default=0)
    viewed_scripts = orm.relationship("Script",
                                      secondary=script_view, back_populates="viewed_users")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_photo(self, photo_path):
        # подготовка папки для фото
        directory_for_photos_path = f"static/images/users/{self.id}"
        if os.path.exists(directory_for_photos_path):
            previous_photos = os.listdir(directory_for_photos_path)
            for photo_to_remove in previous_photos:
                file_path = os.path.join(directory_for_photos_path, photo_to_remove)
                os.remove(file_path)
        else:
            os.makedirs(directory_for_photos_path)

        extension = photo_path.split(".")[-1]
        types_of_photos_and_sizes = {"big_photo": (300, 450),
                                     "middle_photo": (150, 225),
                                     "small_photo": (60, 60)}

        for type_of_photo in types_of_photos_and_sizes:
            unique_id = uuid.uuid4()
            new_path = f"{directory_for_photos_path}/{type_of_photo}_{unique_id}.{extension}"
            change_image_size(photo_path, new_path, *types_of_photos_and_sizes[type_of_photo])
            self.__setattr__(f"{type_of_photo}_path", new_path.lstrip("static"))



