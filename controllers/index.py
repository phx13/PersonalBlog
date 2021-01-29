from flask import Blueprint, render_template
from models.blog import Blog

index = Blueprint('index', __name__)


@index.route('/')
def indexpage():
    blog_instance = Blog()
    blogs = blog_instance.search_blog_by_limit(0, 4)
    return render_template('index.html', blogs=blogs)
