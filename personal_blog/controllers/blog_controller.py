import time

from flask import Blueprint, render_template, abort, session

from personal_blog.models.account_model import AccountModel
from personal_blog.models.blog_model import BlogModel
from personal_blog.models.collection_model import CollectionModel
from personal_blog.models.comment_model import CommentModel
import math

from personal_blog.models.credit_model import CreditModel

blog_blueprint = Blueprint('blog_blueprint', __name__)


@blog_blueprint.route('/blog')
def blog_page():
    blog_model = BlogModel()
    blogs_per_page = 6
    current_page_blogs = blog_model.search_blog_by_limit(0, blogs_per_page)
    total_page = math.ceil(blog_model.search_blog_total_count() / blogs_per_page)
    return render_template('blog.html', current_page_blogs=current_page_blogs, current_page=1, total_page=total_page)


@blog_blueprint.route('/blog/<int:current_page>')
def blog_current_page(current_page):
    blog_model = BlogModel()
    blogs_per_page = 6
    offset_count = (current_page - 1) * blogs_per_page
    current_page_blogs = blog_model.search_blog_by_limit(offset_count, blogs_per_page)
    total_page = math.ceil(blog_model.search_blog_total_count() / blogs_per_page)
    return render_template('blog.html', current_page_blogs=current_page_blogs, current_page=current_page, total_page=total_page)


@blog_blueprint.route('/blog-search/<int:current_page>-<keyword>')
def blog_current_page_by_search(current_page, keyword):
    keyword = keyword.strip()
    if keyword is None or keyword == "" or '%' in keyword or len(keyword) > 10:
        abort(404)
    blog_model = BlogModel()
    blogs_per_page = 6
    offset_count = (current_page - 1) * blogs_per_page
    current_page_blogs = blog_model.search_blog_by_query_article(keyword, offset_count, blogs_per_page)
    total_page = math.ceil(blog_model.search_blog_total_count_by_article(keyword) / blogs_per_page)
    return render_template('blog_search.html', current_page_blogs=current_page_blogs, current_page=current_page, total_page=total_page, keyword=keyword)


@blog_blueprint.route('/blog-type/<int:current_page>-<type>')
def blog_current_page_by_type(current_page, type):
    try:
        blog_model = BlogModel()
        blogs_per_page = 6
        offset_count = (current_page - 1) * blogs_per_page
        current_page_blogs = blog_model.search_blog_by_type(type, offset_count, blogs_per_page)
        total_page = math.ceil(blog_model.search_blog_total_count_by_type(type) / blogs_per_page)
    except:
        abort(500)
    return render_template('blog_type.html', current_page_blogs=current_page_blogs, current_page=current_page, total_page=total_page, type=type)


@blog_blueprint.route('/blog-article/<int:id>')
def blog_article_page(id):
    try:
        blog_model = BlogModel()
        blog_article = blog_model.search_blog_by_id(id)
        if blog_article is None:
            abort(404)
    except:
        abort(500)

    blog_model.update_blog_read_count(id)
    collection_model = CollectionModel()
    is_collection = collection_model.check_collection(id, session.get('email'))
    comment_model = CommentModel()
    comment_reply_list = comment_model.get_comment_with_reply(id, 0, 10)
    return render_template('blog_article.html', blog_article=blog_article, is_collection=is_collection, comment_reply_list=comment_reply_list)


@blog_blueprint.route('/blog-article/<int:id>/<int:rate>', methods=['POST'])
def blog_article_rate(id, rate):
    try:
        blog_model = BlogModel()
        blog_article = blog_model.search_blog_by_id(id)
        if blog_article is None:
            abort(404)
    except:
        abort(500)

    rate = (blog_article.rate * blog_article.ratecount + rate) / (blog_article.ratecount + 1)
    blog_model.update_blog_rate(id, rate)

    create_time = time.strftime('%Y-%m-%d %H:%M:%S')
    credit_model = CreditModel()
    credit_model.insert_credit(session.get('email'), 'blog', 'rate blog', id, 5, create_time)

    account_model = AccountModel()
    account_model.update_credit(session.get('email'), 5)

    return 'Success: Rate successful, credit +5'
