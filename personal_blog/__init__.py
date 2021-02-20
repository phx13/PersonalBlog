import os
from flask import Flask, render_template, request, session
import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='views', static_url_path='/', static_folder='resources')
app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:phx25891863@localhost:3306/cw2?charset=utf8'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2068740:Phx25891863@csmysql.cs.cf.ac.uk:3306/c2068740_cw2?charset=utf8'
app.config['SQLALCHEMY_POOL_SIZE'] = 1000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.errorhandler(404)
def error404(e):
    return render_template('error404.html')


@app.errorhandler(500)
def error500(e):
    return render_template('error500.html')


@app.before_request
def before_request():
    url = request.path
    can_pass_urls = ['/login', '/register', '/logout']
    if url in can_pass_urls or url.endswith('.js') or url.endswith('.jpg') or url.endswith('.png'):
        pass
    elif session.get('login') is None:
        from personal_blog.models.account_model import AccountModel
        account_model = AccountModel()
        email = request.cookies.get('email')
        if email is not None:
            result = account_model.search_account_by_email(email)
            session['login'] = 'true'
            session['email'] = result.email
            session['nickname'] = result.nickname


from personal_blog.controllers.index_controller import index_blueprint
from personal_blog.controllers.account_controller import account_blueprint
from personal_blog.controllers.blog_controller import blog_blueprint
from personal_blog.controllers.post_blog_controller import post_blog_blueprint
from personal_blog.controllers.collection_controller import collection_blueprint
from personal_blog.controllers.comment_controller import comment_blueprint

app.register_blueprint(index_blueprint)
app.register_blueprint(account_blueprint)
app.register_blueprint(blog_blueprint)
app.register_blueprint(post_blog_blueprint)
app.register_blueprint(collection_blueprint)
app.register_blueprint(comment_blueprint)
