import datetime

from sqlalchemy import Table, Column, ForeignKey, Integer, DateTime
from data.db_session import SqlAlchemyBase


script_view = Table('script_view', SqlAlchemyBase.metadata,
                     Column('viewed_user_id', Integer, ForeignKey('users.id'), primary_key=True),
                     Column('viewed_script_id', Integer, ForeignKey('scripts.id'), primary_key=True),
                     Column("date", DateTime, default=lambda: datetime.datetime.now().date(), nullable=False))
