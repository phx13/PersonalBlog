from flask import session
from sqlalchemy import Table
from personal_blog.commons.db_orm_helper import init_db, join_list_model
from personal_blog.models.account_model import AccountModel

db_session, db_model, db_metadata = init_db()


class CreditModel(db_model):
    __tablename__ = 'credit'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def insert_credit(self, type, event, credit, time):
        credit_model = CreditModel(email=session.get('email'), type=type, event=event, credit=credit, createtime=time, updatetime=time)
        db_session.add(credit_model)
        db_session.commit()
