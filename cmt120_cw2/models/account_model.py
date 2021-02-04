from sqlalchemy import Table
from commons.db_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class AccountModel(db_model):
    __tablename__ = 'account'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def search_account_by_email(self, email):
        result = db_session.query(AccountModel).filter_by(email=email).all()
        return result

    def register_account(self, email, password, nickname, avatar, profile, create_time):
        account_model = AccountModel(email=email, password=password, nickname=nickname, avatar=avatar,
                                              profile=profile, createtime=create_time)
        db_session.add(account_model)
        db_session.commit()

    def update_account(self, email, avatar, nickname, password, profile, update_time):
        result = db_session.query(AccountModel).filter_by(email=email).update(
            {'avatar': avatar, 'nickname': nickname, 'password': password, 'profile': profile,
             'updatetime': update_time})
        db_session.commit()
        return result
