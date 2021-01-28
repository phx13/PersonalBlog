

from sqlalchemy import Table

from commons.database_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class User(db_model):
    __tablename__ = 'user'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def search_user_by_email(self, email):
        result = db_session.query(User).filter_by(email=email).all()
        return result

    def register(self, email, password, nickname, avater, profile, create_time):
        user_instance = User(email=email, password=password, nickname=nickname, avater=avater, profile=profile,
                             createtime=create_time)
        db_session.add(user_instance)
        db_session.commit()
        return user_instance

    def update(self, email, avater, nickname, password, profile, update_time):
        result = db_session.query(User).filter_by(email=email).update(
            {'avater': avater, 'nickname': nickname, 'password': password, 'profile': profile,
             'updatetime': update_time})
        db_session.commit()
        return result
