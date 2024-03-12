import datetime
from typing import List
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import Mapped
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Colomn(ProfileImage, nullable=False)
    social_networks = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    
    rating = sqlalchemy.Colomn(sqlalchemy.Integer,
                                nullable=False)
    
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True,
                            unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    scripts = orm.relationship("Script", back_populates='author')


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)