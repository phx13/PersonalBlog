from flask import Blueprint, render_template, request, abort

from personal_blog.commons.verification_helper import EmailContactHelper
from personal_blog.models.blog_model import BlogModel

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/')
def index_page():
    blog_model = BlogModel()
    index_page_blogs = blog_model.search_blog_by_hot(0, 4)
    types = blog_model.search_all_type()
    return render_template('index.html', index_page_blogs=index_page_blogs, types=types, is_home=True)


@index_blueprint.route('/contact', methods=['POST'])
def contact():
    try:
        email = request.form.get('email').strip()
        name = request.form.get('name').strip()
        message = request.form.get('message').strip()
        EmailContactHelper().send_email(email, name, message)
        return 'Success (Server) : Contact email send successful'
    except:
        return 'Fail (Server) : Contact email send failed'
