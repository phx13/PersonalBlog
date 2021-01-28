import time

from sqlalchemy import Table

from commons.database_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class Blog(db_model):
    __tablename__ = 'blog'
    __table__ = Table(__tablename__, db_metadata, autoload=True)