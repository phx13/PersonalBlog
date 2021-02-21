from sqlalchemy import Table

from personal_blog.commons.db_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class CreditModel(db_model):
    __tablename__ = 'credit'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def insert_credit(self, email, type, event, target, credit, time):
        credit_model = CreditModel(email=email, type=type, event=event, target=target, credit=credit, createtime=time, updatetime=time)
        db_session.add(credit_model)
        db_session.commit()

    def check_credit(self, email, type, target):
        result = db_session.query(CreditModel).filter_by(email=email, type=type, target=target).first()
        return result

    def check_credit_by_time(self, email, type, start_time, end_time):
        result = db_session.query(CreditModel).filter(CreditModel.email == email, CreditModel.type == type,
                                                      CreditModel.createtime.between(start_time, end_time)).all()
        return result

    def search_credit_by_email(self, email):
        result = db_session.query(CreditModel).filter_by(email=email).order_by(CreditModel.updatetime.desc()).all()
        return result
