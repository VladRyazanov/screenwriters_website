from sqlalchemy import Table, Column, ForeignKey, Integer
from data.db_session import SqlAlchemyBase


subscription = Table('subscription', SqlAlchemyBase.metadata,
                     Column('subscriber_id', Integer, ForeignKey('users.id'), primary_key=True),
                     Column('subscribed_to_id', Integer, ForeignKey('users.id'), primary_key=True))