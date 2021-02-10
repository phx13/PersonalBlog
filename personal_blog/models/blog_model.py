from sqlalchemy import Table
from personal_blog.commons.db_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class BlogModel(db_model):
    __tablename__ = 'blog'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    # 查询所有博客
    def search_all_blog(self):
        result = db_session.query(BlogModel).all()
        return result

    # 查询文章总数量
    def search_blog_total_count(self):
        result = db_session.query(BlogModel).count()
        return result

    # 根据id查询博客
    def search_blog_by_id(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        return result

    # 查询指定数量的最新博客
    def search_blog_by_limit(self, start, count):
        result = db_session.query(BlogModel).order_by(BlogModel.updatetime.desc()).limit(count).offset(start)
        return result

    # 根据模糊搜索标题查询指定数量的博客
    def search_blog_by_query_article(self, keyword, start, count):
        result = db_session.query(BlogModel).filter(BlogModel.article.like('%' + keyword + '%')).order_by(BlogModel.updatetime.desc()).limit(count).offset(start)
        return result

    # 根据模糊查询标题查询文章总数量
    def search_blog_total_count_by_article(self, keyword):
        result = db_session.query(BlogModel).filter(BlogModel.article.like('%' + keyword + '%')).count()
        return result

    # 根据类别查询指定数量的博客
    def search_blog_by_type(self, type, start, count):
        result = db_session.query(BlogModel).filter(BlogModel.type.like('%' + type + '%')).order_by(BlogModel.updatetime.desc()).limit(count).offset(start)
        return result

    # 根据类别查询文章总数量
    def search_blog_total_count_by_type(self, type):
        result = db_session.query(BlogModel).filter(BlogModel.type.like('%' + type + '%')).count()
        return result

    # 更新阅读次数
    def update_blog_read_count(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        result.readcount += 1
        db_session.commit()
