from flask import Blueprint, render_template, abort
from personal_blog.models.blog_model import BlogModel
from personal_blog.models.collection_model import CollectionModel
import math



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
    is_collection = collection_model.check_collection(id)
    return render_template('blog_article.html', blog_article=blog_article, is_collection=is_collection)
