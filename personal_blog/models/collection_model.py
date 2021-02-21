from sqlalchemy import Table

from personal_blog.commons.db_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class CollectionModel(db_model):
    __tablename__ = 'collection'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def insert_collection(self, article_id, email, time):
        result = db_session.query(CollectionModel).filter_by(articleid=article_id, email=email).first()
        if result is not None:
            result.cancel = 0
            result.updatetime = time
        else:
            collection_model = CollectionModel(articleid=article_id, email=email, cancel=0, createtime=time, updatetime=time)
            db_session.add(collection_model)
        db_session.commit()

    def cancel_collection(self, article_id, email, time):
        result = db_session.query(CollectionModel).filter_by(articleid=article_id, email=email).first()
        if result is not None:
            result.cancel = 1
            result.updatetime = time
        db_session.commit()

    def check_collection(self, article_id, email):
        result = db_session.query(CollectionModel).filter_by(articleid=article_id, email=email).first()
        if result is None or result.cancel == 1:
            return False
        return True

    def search_collection_by_email(self, email):
        result = db_session.query(CollectionModel).filter_by(email=email, cancel=0).order_by(CollectionModel.updatetime.desc()).all()
        return result
