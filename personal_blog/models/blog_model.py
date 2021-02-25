from sqlalchemy import Table, distinct

from personal_blog.commons.db_orm_helper import init_db

db_session, db_model, db_metadata = init_db()


class BlogModel(db_model):
    __tablename__ = 'blog'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def search_all_blog(self):
        result = db_session.query(BlogModel).filter_by(draft=0).all()
        return result

    def search_all_draft_blog(self):
        result = db_session.query(BlogModel).filter_by(draft=1).all()
        return result

    def search_all_type(self):
        result = db_session.query(distinct(BlogModel.type)).filter_by(draft=0).all()
        res = []
        for item in result:
            for subtype in item[0].strip().split(','):
                if subtype not in res:
                    res.append(subtype)
        result = ','.join(res)
        return result

    def search_blog_total_count(self):
        result = db_session.query(BlogModel).filter_by(draft=0).count()
        return result

    def search_blog_by_id(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        return result

    def search_blog_by_hot(self, start, count):
        result = db_session.query(BlogModel).filter_by(draft=0).order_by(BlogModel.readcount.desc()).limit(count).offset(start)
        return result

    def search_blog_by_limit(self, start, count, sort):
        if sort == 1:
            result = db_session.query(BlogModel).filter_by(draft=0).order_by(BlogModel.updatetime.desc()).limit(count).offset(start)
        else:
            result = db_session.query(BlogModel).filter_by(draft=0).order_by(BlogModel.updatetime.asc()).limit(count).offset(start)
        return result

    def search_blog_by_article(self, keyword, start, count, sort):
        if sort == 1:
            result = db_session.query(BlogModel).filter(BlogModel.article.like('%' + keyword + '%'), BlogModel.draft == 0).order_by(BlogModel.updatetime.desc()).limit(
                count).offset(start)
        else:
            result = db_session.query(BlogModel).filter(BlogModel.article.like('%' + keyword + '%'), BlogModel.draft == 0).order_by(BlogModel.updatetime.asc()).limit(
                count).offset(start)
        return result

    def search_blog_total_count_by_article(self, keyword):
        result = db_session.query(BlogModel).filter(BlogModel.article.like('%' + keyword + '%'), BlogModel.draft == 0).count()
        return result

    def search_blog_by_content(self, keyword, start, count, sort):
        if sort == 1:
            result = db_session.query(BlogModel).filter(BlogModel.content.like('%' + keyword + '%'), BlogModel.draft == 0).order_by(BlogModel.updatetime.desc()).limit(
                count).offset(start)
        else:
            result = db_session.query(BlogModel).filter(BlogModel.content.like('%' + keyword + '%'), BlogModel.draft == 0).order_by(BlogModel.updatetime.asc()).limit(
                count).offset(start)
        return result

    def search_blog_total_count_by_content(self, keyword):
        result = db_session.query(BlogModel).filter(BlogModel.content.like('%' + keyword + '%'), BlogModel.draft == 0).count()
        return result

    def search_blog_by_type(self, type, start, count, sort):
        if sort == 1:
            result = db_session.query(BlogModel).filter(BlogModel.type.like('%' + type + '%'), BlogModel.draft == 0).order_by(BlogModel.updatetime.desc()).limit(count).offset(
                start)
        else:
            result = db_session.query(BlogModel).filter(BlogModel.type.like('%' + type + '%'), BlogModel.draft == 0).order_by(BlogModel.updatetime.asc()).limit(count).offset(
                start)
        return result

    def search_blog_total_count_by_type(self, type):
        result = db_session.query(BlogModel).filter(BlogModel.type.like('%' + type + '%'), BlogModel.draft == 0).count()
        return result

    def update_blog_read_count(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        result.readcount += 1
        db_session.commit()

    def update_blog_reply_count(self, id):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        result.replycount += 1
        db_session.commit()

    def update_blog_rate(self, id, rate):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        result.rate = rate
        result.ratecount += 1
        db_session.commit()

    def post_blog(self, article, type, content, thumb, rate, rate_count, read_count, reply_count, draft, time):
        blog_model = BlogModel(article=article, type=type, content=content, thumb=thumb, rate=rate, ratecount=rate_count, readcount=read_count, replycount=reply_count, draft=draft,
                               createtime=time, updatetime=time)
        db_session.add(blog_model)
        db_session.commit()

    def update_blog(self, id, article, type, content, thumb, draft, time):
        result = db_session.query(BlogModel).filter_by(id=id).update({'article': article, 'type': type, 'content': content, 'thumb': thumb, 'draft': draft, 'updatetime': time})
        db_session.commit()
        return result

    def update_blog_draft(self, id, draft):
        result = db_session.query(BlogModel).filter_by(id=id).first()
        result.draft = draft
        db_session.commit()
