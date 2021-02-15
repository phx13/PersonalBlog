from flask import session
from sqlalchemy import Table
from personal_blog.commons.db_orm_helper import init_db
from personal_blog.models.account_model import AccountModel

db_session, db_model, db_metadata = init_db()


class CommentModel(db_model):
    __tablename__ = 'comment'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def insert_comment(self, article_id, content, time):
        comment_model = CommentModel(email=session.get('email'), articleid=article_id, content=content, createtime=time, updatetime=time)
        db_session.add(comment_model)
        db_session.commit()

    def search_comment_by_article(self, article_id):
        result = db_session.query(CommentModel).filter_by(articleid=article_id, replyid=0).all()
        return result

    def check_limit_comment(self, start_time, end_time):
        result = db_session.query(CommentModel).filter(CommentModel.email == session.get('email'), CommentModel.createtime.between(start_time, end_time)).all()
        if len(result) > 10:
            return True
        return False

    def search_comment_with_account_by_limit(self, article_id, start, count):
        result = db_session.query(CommentModel, AccountModel).join(AccountModel, AccountModel.email == CommentModel.email).filter(CommentModel.articleid == article_id).order_by(
            CommentModel.updatetime.desc()).limit(count).offset(start).all()
        return result
