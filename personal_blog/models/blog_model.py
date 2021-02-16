from sqlalchemy import Table
from personal_blog.commons.db_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class BlogModel(db_model):
    __tablename__ = 'blog'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def search_all_blog(self):
        result = db_session.query(BlogModel).all()
        return result

    def search_blog_total_count(self):
        result = db_session.query(BlogModel).count()
        return result

    def search_blog_by_id(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        return result

    def search_blog_by_limit(self, start, count):
        result = db_session.query(BlogModel).order_by(BlogModel.updatetime.desc()).limit(count).offset(start)
        return result

    def search_blog_by_query_article(self, keyword, start, count):
        result = db_session.query(BlogModel).filter(BlogModel.article.like('%' + keyword + '%')).order_by(BlogModel.updatetime.desc()).limit(count).offset(start)
        return result

    def search_blog_total_count_by_article(self, keyword):
        result = db_session.query(BlogModel).filter(BlogModel.article.like('%' + keyword + '%')).count()
        return result

    def search_blog_by_type(self, type, start, count):
        result = db_session.query(BlogModel).filter(BlogModel.type.like('%' + type + '%')).order_by(BlogModel.updatetime.desc()).limit(count).offset(start)
        return result

    def search_blog_total_count_by_type(self, type):
        result = db_session.query(BlogModel).filter(BlogModel.type.like('%' + type + '%')).count()
        return result

    def update_blog_read_count(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        result.readcount += 1
        db_session.commit()

    def update_blog_reply_count(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        result.replycount += 1
        db_session.commit()
