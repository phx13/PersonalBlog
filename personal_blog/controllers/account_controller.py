import hashlib
import re
import time

from flask import Blueprint, request, session, url_for, make_response, render_template, abort

from personal_blog.commons.base64_helper import Base64Helper
from personal_blog.commons.verification_helper import ImageVerificationHelper, EmailVerificationHelper
from personal_blog.models.account_model import AccountModel
from personal_blog.models.collection_model import CollectionModel
from personal_blog.models.credit_model import CreditModel

account_blueprint = Blueprint('account_blueprint', __name__)


@account_blueprint.route('/login', methods=['POST'])
def login():
    account_model = AccountModel()
    email = request.form.get('email').strip()
    password = request.form.get('password').strip()
    password = hashlib.md5(password.encode()).hexdigest()
    image_code = request.form.get('image_code').lower().strip()
    result = account_model.search_account_by_email(email)

    if image_code == session.get('image_code'):
        if result and result.password == password:
            session['login'] = 'true'
            session['email'] = result.email
            session['nickname'] = result.nickname

            create_time = time.strftime('%Y-%m-%d %H:%M:%S')
            start_time = time.strftime('%Y-%m-%d 00:00:00')
            end_time = time.strftime('%Y-%m-%d 23:59:59')
            credit_model = CreditModel()
            if len(credit_model.check_credit_by_time(session.get('email'), 'login', start_time, end_time)) == 0:
                credit_model.insert_credit(session.get('email'), 'login', 'today\'s first login', 0, 5, create_time)
                account_model.update_credit(session.get('email'), 5)
                response = make_response('Success: Today\'s first login, credit +5')
            else:
                response = make_response('Success: Login successful')

            response.set_cookie('email', result.email, max_age=10 * 24 * 3600)
            return response
        else:
            return 'Fail: The account does not exist or the password is wrong'
    return 'Fail: Incorrect image verification code'


@account_blueprint.route('/register', methods=['POST'])
def register():
    account_model = AccountModel()
    email = request.form.get('email').strip()
    password = request.form.get('password').strip()
    email_code = request.form.get('email_code').strip()

    if account_model.search_account_by_email(email):
        return 'Fail: This account is already registered'
    elif not re.match('.+@.+\..+', email) or len(password) < 3:
        return 'Fail: Invalid email or password less than 3 letters'
    elif email_code != session.get('email_code'):
        return 'Fail: Incorrect email verification code'
    else:
        password = hashlib.md5(password.encode()).hexdigest()
        nickname = email.split('@')[0]
        avatar = '/images/cardiff_university_logo.jpg'
        profile = 'Hello, this is ' + nickname
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')
        account_model.register_account(email, password, nickname, avatar, profile, 0, create_time)

        session['login'] = 'true'
        session['email'] = email
        session['nickname'] = nickname

        credit_model = CreditModel()
        credit_model.insert_credit(session.get('email'), 'register', 'new register', 0, 50, create_time)
        account_model.update_credit(session.get('email'), 50)

        response = make_response('Success: Register successful, credit +50')
        response.set_cookie('email', email, max_age=10 * 24 * 3600)
        return response


@account_blueprint.route('/verification/image')
def verification_code():
    try:
        code, byte_code = ImageVerificationHelper().get_code()
        response = make_response(byte_code)
        response.headers['Content-type'] = 'image/jpeg'
        session['image_code'] = code.lower()
    except:
        return 'Fail: Image generate failed'
    return response


@account_blueprint.route('/verification/email', methods=['POST'])
def verification_email():
    try:
        email = request.form.get('email')
        code = EmailVerificationHelper().generate_code()
        EmailVerificationHelper().send_email(email, code)
        session['email_code'] = code
        return 'Success: Email send successful'
    except:
        return 'Fail: Email send failed'


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
    credit_model = CreditModel()
    credit_activities = credit_model.search_credit_by_email(session.get('email'))
    collection_model = CollectionModel()
    collection_activities = collection_model.search_collection_by_email(session.get('email'))
    return render_template('account.html', current_account=current_account, credit_activities=credit_activities, collection_activities=collection_activities)


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
