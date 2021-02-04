from flask import Blueprint, render_template
from cmt120_cw2.models.blog_model import BlogModel

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/')
def index_page():
    blog_model = BlogModel()
    index_page_blogs = blog_model.search_blog_by_limit(0, 6)
    return render_template('index.html', index_page_blogs=index_page_blogs)
