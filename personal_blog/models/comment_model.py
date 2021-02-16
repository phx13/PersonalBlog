from flask import session
from sqlalchemy import Table
from personal_blog.commons.db_orm_helper import init_db, join_list_model
from personal_blog.models.account_model import AccountModel

db_session, db_model, db_metadata = init_db()


class CommentModel(db_model):
    __tablename__ = 'comment'
    __table__ = Table(__tablename__, db_metadata, autoload=True)

    def insert_comment(self, article_id, content, time):
        comment_model = CommentModel(email=session.get('email'), articleid=article_id, content=content, replyid=0, agreecount=0, disagreecount=0, createtime=time, updatetime=time)
        db_session.add(comment_model)
        db_session.commit()

    def search_comment_by_article(self, article_id):
        result = db_session.query(CommentModel).filter_by(articleid=article_id, replyid=0).all()
        return result

    def search_comment_by_id(self, id):
        result = db_session.query(CommentModel).filter_by(id=id).first()
        return result

    def check_limit_comment(self, start_time, end_time):
        result = db_session.query(CommentModel).filter(CommentModel.email == session.get('email'), CommentModel.createtime.between(start_time, end_time)).all()
        if len(result) > 10:
            return True
        return False

    def search_comment_with_account_by_limit(self, article_id, start, count):
        result = db_session.query(CommentModel, AccountModel).join(AccountModel, AccountModel.email == CommentModel.email).filter(CommentModel.articleid == article_id,
                                                                                                                                  CommentModel.replyid == 0).order_by(
            CommentModel.updatetime.desc()).limit(count).offset(start).all()
        return result

    def insert_reply(self, article_id, comment_id, content, time):
        comment_model = CommentModel(email=session.get('email'), articleid=article_id, content=content, replyid=comment_id, agreecount=0, disagreecount=0, createtime=time,
                                     updatetime=time)
        db_session.add(comment_model)
        db_session.commit()

    def search_reply_with_account(self, reply_id):
        result = db_session.query(CommentModel, AccountModel).join(AccountModel, AccountModel.email == CommentModel.email).filter(CommentModel.replyid == reply_id).order_by(
            CommentModel.updatetime.desc()).all()
        return result

    def get_comment_with_reply(self, article_id, start, count):
        result = self.search_comment_with_account_by_limit(article_id, start, count)
        comment_reply_list = join_list_model(result)
        for comment in comment_reply_list:
            reply_list_dict = []
            comment_result = self.search_reply_with_account(comment['id'])
            for reply in join_list_model(comment_result):
                respondent_email = self.search_comment_by_id(reply['replyid']).email
                account_model = AccountModel()
                reply['respondent'] = account_model.search_account_by_email(respondent_email)
                reply_list_dict.append(reply)

                reply_result = self.search_reply_with_account(reply['id'])
                for reply_reply in join_list_model(reply_result):
                    respondent_email = self.search_comment_by_id(reply_reply['replyid']).email
                    reply_reply['respondent'] = account_model.search_account_by_email(respondent_email)
                    reply_list_dict.append(reply_reply)
            comment['reply_list'] = reply_list_dict
        return comment_reply_list
