import datetime

from flask_login import UserMixin
from sqlalchemy import orm, Integer, String, Column, DateTime
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase
from data.subscription import subscription
from data.script_view import script_view


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    photo_path = Column(String)
    social_networks = Column(String, nullable=True)
    rating = Column(Integer, default=0)
    given_script_marks = orm.relationship("ScriptMark", back_populates="user")
    given_script_reviews = orm.relationship("ScriptReview", back_populates="user")
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    modified_date = Column(DateTime, default=datetime.datetime.now)

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
