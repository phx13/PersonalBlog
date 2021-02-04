import hashlib
import re
import time

from flask import Blueprint, request, session, url_for, make_response
from personal_blog.models.account_model import AccountModel

account_blueprint = Blueprint('account_blueprint', __name__)


@account_blueprint.route('/login', methods=['POST'])
def login():
    account_model = AccountModel()
    email = request.form.get('email')
    password = request.form.get('password')
    password = hashlib.md5(password.encode()).hexdigest()
    result = account_model.search_account_by_email(email)

    if len(result) == 1 and result[0].password == password:
        session['login'] = 'true'
        session['email'] = result[0].email
        session['nickname'] = result[0].nickname

        response = make_response('Success: Login successful')
        response.set_cookie('email', result[0].email, max_age=10 * 24 * 3600)
        response.set_cookie('password', result[0].password, max_age=10 * 24 * 3600)
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
        account_model.register_account(email, password, nickname, avatar, profile, create_time)

        session['login'] = 'true'
        session['email'] = email
        session['nickname'] = nickname

        response = make_response('Success: Register successful')
        response.set_cookie('email', email, max_age=10 * 24 * 3600)
        response.set_cookie('password', password, max_age=10 * 24 * 3600)
        return response


@account_blueprint.route('/logout')
def logout():
    session.clear()
    response = make_response('logout', 302)
    response.headers['Location'] = url_for('index_blueprint.index_page')
    response.delete_cookie('email')
    response.delete_cookie('password')
    return response
