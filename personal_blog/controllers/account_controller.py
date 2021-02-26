import hashlib
import re
import time

from flask import Blueprint, request, session, url_for, make_response, render_template

from personal_blog.commons.base64_helper import Base64Helper
from personal_blog.commons.verification_helper import ImageVerificationHelper, EmailVerificationHelper, ForgetPasswordHelper
from personal_blog.models.account_model import AccountModel
from personal_blog.models.collection_model import CollectionModel
from personal_blog.models.credit_model import CreditModel

account_blueprint = Blueprint('account_blueprint', __name__)


@account_blueprint.route('/login', methods=['POST'])
def login():
    try:
        account_model = AccountModel()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        password = hashlib.md5(password.encode()).hexdigest()
        image_code = request.form.get('image_code').lower().strip()
        result = account_model.search_account_by_email(email)

        if image_code != session.get('image_code'):
            return 'Fail (Server) : Incorrect image verification code'
        elif not result:
            return 'Fail (Server) : Account does not exist'
        elif result.password != password:
            return 'Fail (Server) : Password is wrong'
        else:
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
                response = make_response('Success (Server) : Today\'s first login, credit +5')
            else:
                response = make_response('Success (Server) : Login successful')

            response.set_cookie('email', result.email, max_age=10 * 24 * 3600)
            return response
    except:
        return 'Fail (Server) : Login failed'


@account_blueprint.route('/register', methods=['POST'])
def register():
    try:
        account_model = AccountModel()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        name = request.form.get('name').strip()
        email_code = request.form.get('email_code').strip()

        if account_model.search_account_by_email(email):
            return 'Fail (Server) : Account is exist'
        elif not re.match('.+@.+\..+', email):
            return 'Fail (Server) : Invalid email'
        elif len(password) < 3:
            return 'Fail (Server) : Password less than 3 letters'
        elif email_code != session.get('email_code'):
            return 'Fail (Server) : Incorrect email verification code'
        else:
            password = hashlib.md5(password.encode()).hexdigest()
            nickname = name
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

            response = make_response('Success (Server) : Register successful, credit +50')
            response.set_cookie('email', email, max_age=10 * 24 * 3600)
            return response
    except:
        return 'Fail (Server) : Register failed'


@account_blueprint.route('/verification/image')
def verification_code():
    try:
        code, base64_str = ImageVerificationHelper().get_code()
        session['image_code'] = code.lower()
        return base64_str
    except:
        return 'Fail (Server) : Image code generate failed'


@account_blueprint.route('/verification/email', methods=['POST'])
def verification_email():
    try:
        email = request.form.get('email').strip()
        if not email:
            return 'Fail (Server) : Invalid email'

        account_model = AccountModel()
        current_account = account_model.search_account_by_email(email)
        if current_account:
            return 'Fail (Server) : Account is existed'

        code = EmailVerificationHelper().generate_code()
        session['email_code'] = code
        EmailVerificationHelper().send_email(email, code)
        return 'Success (Server) : Verification email send successful, code is ' + session.get('email_code')
    except:
        return 'Fail (Server) : Verification email send failed'


@account_blueprint.route('/forget', methods=['POST'])
def forget():
    try:
        email = request.form.get('email').strip()
        if not email:
            return 'Fail (Server) : Invalid email'

        account_model = AccountModel()
        current_account = account_model.search_account_by_email(email)
        if not current_account:
            return 'Fail (Server) : Account is not existed'

        password = ForgetPasswordHelper().generate_password()
        ForgetPasswordHelper().send_email(email, password)

        password = hashlib.md5(password.encode()).hexdigest()
        update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        account_model.update_account(current_account.email, current_account.avatar, current_account.nickname, password, current_account.profile, update_time)
        return 'Success (Server) : Password email send successful'
    except:
        return 'Fail (Server) : Password email send failed'


@account_blueprint.route('/logout')
def logout():
    try:
        session.clear()
        response = make_response('logout', 302)
        response.headers['Location'] = url_for('index_blueprint.index_page')
        response.delete_cookie('email')
        return response
    except:
        return 'Fail (Server) : Logout failed'


@account_blueprint.route('/account')
def account_page():
    try:
        account_model = AccountModel()
        current_account = account_model.search_account_by_email(session.get('email'))
        if not current_account:
            return 'Fail (Server) : Account is not existed'

        credit_model = CreditModel()
        credit_activities = credit_model.search_credit_by_email(session.get('email'))
        collection_model = CollectionModel()
        collection_activities = collection_model.search_collection_by_email(session.get('email'))
        return render_template('account.html', current_account=current_account, credit_activities=credit_activities, collection_activities=collection_activities)
    except:
        return 'Fail (Server) : Account page init failed'


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
    return 'Success (Server) : Update profile successful'
