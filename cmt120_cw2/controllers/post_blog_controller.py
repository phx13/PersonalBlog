from flask import Blueprint, render_template
from models.blog_model import BlogModel

post_blog_blueprint = Blueprint('post_blog_blueprint', __name__)


@post_blog_blueprint.route('/post-blog')
def post_blog_page():
    return render_template('post_blog.html')
