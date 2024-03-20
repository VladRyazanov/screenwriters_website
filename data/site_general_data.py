from sqlalchemy import Table, Column, ForeignKey, Integer
from data.db_session import SqlAlchemyBase


site_general_data = Table('site_general_data', SqlAlchemyBase.metadata,
                     Column("total_users_count", Integer, default=1),
                     Column('total_scripts_count', Integer, default=1))
