import hashlib
import re
import time

from flask import Blueprint, request, session, url_for, make_response
from personal_blog.models.comment_model import CommentModel
from personal_blog.models.blog_model import BlogModel

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
            if not comment_model.check_limit_comment(start_time, end_time):
                comment_model.insert_comment(article_id, content, create_time)
                blog_model = BlogModel()
                blog_model.update_blog_reply_count(article_id)
                return 'Success: Comment successful'
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
            if not comment_model.check_limit_comment(start_time, end_time):
                comment_model.insert_reply(article_id, comment_id, content, create_time)
                blog_model = BlogModel()
                blog_model.update_blog_reply_count(article_id)
                return 'Success: Reply successful'
            else:
                return 'Fail: Today\'s reply over 10'
        except:
            return 'Fail: Reply failed'
    return 'Fail: You are not login'
