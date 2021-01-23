import time

from sqlalchemy import Table

from commons.database_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class User(db_model):
    __tablename__ = 'user'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def search_user_by_email(self, email):
        result = db_session.query(User).filter_by(email=email).all()
        return result

    def register(self, email, password, nickname, image, profile):
        register_time = time.strftime('%Y-%m-%d %H:%M:%S')
        user_instance = User(email=email, password=password, nickname=nickname, image=image, profile=profile,
                    time=register_time)
        db_session.add(user_instance)
        db_session.commit()
        return user_instance

    def update(self, email, imgavatar, nickname, password, profile):
        update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        result = db_session.query(User).filter_by(email=email).update(
            {'image': imgavatar, 'nickname': nickname, 'password': password, 'profile': profile, 'time': update_time})
        db_session.commit()
        return result
