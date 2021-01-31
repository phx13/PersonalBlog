from sqlalchemy import Table

from commons.db_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class BlogModel(db_model):
    __tablename__ = 'blog'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def search_all_blog(self):
        result = db_session.query(BlogModel).all()
        return result

    def search_blog_by_id(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).all()
        return result

    def search_blog_by_limit(self, start, count):
        result = db_session.query(BlogModel).order_by(BlogModel.updatetime.desc()).limit(count).offset(start)
        return result
