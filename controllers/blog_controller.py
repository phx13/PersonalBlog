from flask import Blueprint, render_template
from models.blog_model import BlogModel

blog_blueprint = Blueprint('blog_blueprint', __name__)


@blog_blueprint.route('/blog')
def blog_page():
    blog_model = BlogModel()
    blog_page_blogs = blog_model.search_blog_by_limit(0, 10)
    return render_template('blog.html', blog_page_blogs=blog_page_blogs)
