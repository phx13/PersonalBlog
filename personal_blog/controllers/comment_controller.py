import time

from flask import Blueprint, request, session

from personal_blog.models.account_model import AccountModel
from personal_blog.models.blog_model import BlogModel
from personal_blog.models.comment_model import CommentModel
from personal_blog.models.credit_model import CreditModel

comment_blueprint = Blueprint('comment_blueprint', __name__)


@comment_blueprint.route('/comment', methods=['POST'])
def insert_comment():
    if session.get('login') == 'true':
        try:
            article_id = request.form.get('article_id')
            content = request.form.get('content').strip()
            create_time = time.strftime('%Y-%m-%d %H:%M:%S')
            start_time = time.strftime('%Y-%m-%d 00:00:00')
            end_time = time.strftime('%Y-%m-%d 23:59:59')

            if len(content) < 5 or len(content) > 200:
                return 'Fail: Comment content less than 5 letter or more than 200 letter'

            comment_model = CommentModel()
            if not comment_model.check_limit_comment(session.get('email'), start_time, end_time):
                comment_model.insert_comment(session.get('email'), article_id, content, create_time)
                blog_model = BlogModel()
                blog_model.update_blog_reply_count(article_id)

                credit_model = CreditModel()
                credit_model.insert_credit(session.get('email'), 'comment', 'insert comment', article_id, 5, create_time)
                account_model = AccountModel()
                account_model.update_credit(session.get('email'), 5)
                return 'Success: Comment successful, credit +5'
            else:
                return 'Fail: Today\'s comments over 10'
        except:
            return 'Fail: Comment failed'
    return 'Fail: You are not login'


@comment_blueprint.route('/reply', methods=['POST'])
def insert_reply():
    if session.get('login') == 'true':
        try:
            article_id = request.form.get('article_id')
            comment_id = request.form.get('comment_id')
            content = request.form.get('content').strip()
            create_time = time.strftime('%Y-%m-%d %H:%M:%S')
            start_time = time.strftime('%Y-%m-%d 00:00:00')
            end_time = time.strftime('%Y-%m-%d 23:59:59')

            if len(content) < 5 or len(content) > 200:
                return 'Fail: Reply content less than 5 letter or more than 200 letter'

            comment_model = CommentModel()
            if not comment_model.check_limit_comment(session.get('email'), start_time, end_time):
                comment_model.insert_reply(session.get('email'), article_id, comment_id, content, create_time)
                blog_model = BlogModel()
                blog_model.update_blog_reply_count(article_id)

                credit_model = CreditModel()
                credit_model.insert_credit(session.get('email'), 'comment', 'reply comment', comment_id, 5, create_time)
                account_model = AccountModel()
                account_model.update_credit(session.get('email'), 5)
                return 'Success: Reply successful, credit +5'
            else:
                return 'Fail: Today\'s reply over 10'
        except:
            return 'Fail: Reply failed'
    return 'Fail: You are not login'


@comment_blueprint.route('/opinion', methods=['POST'])
def update_opinion():
    if session.get('login') == 'true':
        try:
            comment_id = request.form.get('comment_id')
            type = request.form.get('type')
            create_time = time.strftime('%Y-%m-%d %H:%M:%S')
            credit_model = CreditModel()
            if credit_model.check_credit(session.get('email'), 'opinion', comment_id):
                return 'Fail: You have opinion on this comment'
            else:
                comment_model = CommentModel()
                comment_model.update_comment_opinion_count(comment_id, type)
                credit_model.insert_credit(session.get('email'), 'opinion', 'update opinion', comment_id, 1, create_time)
                account_model = AccountModel()
                account_model.update_credit(session.get('email'), 1)
            return 'Success: Opinion successful, credit +1'
        except:
            return 'Fail: Opinion failed'
    return 'Fail: You are not login'
