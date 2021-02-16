import hashlib
import re
import time
import base64

from flask import Blueprint, request, session, url_for, make_response, render_template

from personal_blog.commons.base64_helper import Base64Helper
from personal_blog.models.account_model import AccountModel

account_blueprint = Blueprint('account_blueprint', __name__)


@account_blueprint.route('/login', methods=['POST'])
def login():
    account_model = AccountModel()
    email = request.form.get('email')
    password = request.form.get('password')
    password = hashlib.md5(password.encode()).hexdigest()
    result = account_model.search_account_by_email(email)

    if result and result.password == password:
        session['login'] = 'true'
        session['email'] = result.email
        session['nickname'] = result.nickname

        response = make_response('Success: Login successful')
        response.set_cookie('email', result.email, max_age=10 * 24 * 3600)
        return response
    else:
        return 'Fail: The account does not exist or the password is wrong'


@account_blueprint.route('/register', methods=['POST'])
def register():
    account_model = AccountModel()
    email = request.form.get('email')
    password = request.form.get('password')

    if len(account_model.search_account_by_email(email)) > 0:
        return 'Fail: This account is already registered'
    elif not re.match('.+@.+\..+', email) or password == '':
        return 'Fail: Incorrect email or password format'
    else:
        password = hashlib.md5(password.encode()).hexdigest()
        nickname = email.split('@')[0]
        avatar = '/images/cardiff_university_logo.jpg'
        profile = 'Hello, this is ' + nickname
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')
        account_model.register_account(email, password, nickname, avatar, profile, create_time, create_time)

        session['login'] = 'true'
        session['email'] = email
        session['nickname'] = nickname

        response = make_response('Success: Register successful')
        response.set_cookie('email', email, max_age=10 * 24 * 3600)
        return response


@account_blueprint.route('/logout')
def logout():
    session.clear()
    response = make_response('logout', 302)
    response.headers['Location'] = url_for('index_blueprint.index_page')
    response.delete_cookie('email')
    return response


@account_blueprint.route('/account')
def account_page():
    account_model = AccountModel()
    current_account = account_model.search_account_by_email(session.get('email'))
    return render_template('account.html', current_account=current_account)


@account_blueprint.route('/account/profile', methods=['POST'])
def update_profile():
    account_model = AccountModel()
    image = request.form.get('avatar')
    if image == '':
        avatar = account_model.search_account_by_email(session.get('email')).avatar
    else:
        obj = Base64Helper(path='./default.png', choice=2, picture=image)
        avatar = obj.run()
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    if password == '':
        password = account_model.search_account_by_email(session.get('email')).password
    else:
        password = hashlib.md5(password.encode()).hexdigest()
    profile = request.form.get('profile')
    update_time = time.strftime('%Y-%m-%d %H:%M:%S')
    account_model.update_account(session.get('email'), avatar, nickname, password, profile, update_time)
    return 'Success: Update profile successful'
