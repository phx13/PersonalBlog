import time

from sqlalchemy import Table

from commons.database_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class Blog(db_model):
    __tablename__ = 'blog'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def find_all(self):
        result = db_session.query(Blog).all()
        return result

    def search_blog_by_id(self, id):
        result = db_session.query(Blog).filter_by(id=id).all()
        return result

    def search_blog_by_limit(self, start, count):
        result = db_session.query(Blog).order_by(Blog.updatetime.desc()).limit(count).offset(start)
        return result
