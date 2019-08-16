from flask import render_template, request,redirect, url_for, session, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
from werkzeug.urls import url_parse
import datetime
import os
import jwt
from . import auth
from .forms import CreatePasswordForm, SendEmailsForm, LoginForm
from ..email import mail_message
from ..utils import token_url
from ..models import User
from .. import db

# views
@auth.route("/", methods=['GET', 'POST'])
def index():
    send_email_form = SendEmailsForm()
    users = User.query.all()
    # To get user from DB and get email to send emails to
    
    current_user_name ='' 
    expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60)
    for user in users:
        create_pwd_url = token_url(user.id_number, user.email, expiry)
        current_user_name =  user.first_name
        print(create_pwd_url)
        mail_message('iVote', 'email/welcome_user', user.email, url=create_pwd_url)
    print(current_user_name)
    return render_template('index.html', send_email_form=send_email_form, user=current_user_name, url=create_pwd_url)


@auth.route("/create_password", methods=['GET', 'POST'])
def create_password():
    
    if "token" in request.args:
        # Token exist, etxract, decode an redirect to the create password page
        secret_key = os.environ.get("JWT_SECRET")
        algorithm = os.environ.get("JWT_ALGORITHM")
        token = request.args.get("token")
        try:
            payload = jwt.decode(token, secret_key, algorithm=algorithm)
            
            session['email'] = payload["email"]
            session['idno'] = payload["id"]

            # verify user exist with email and id from the payload
            # reditrect user to create password page
            return redirect(url_for("auth.create_user_password"))

        except (jwt.ExpiredSignatureError, jwt.DecodeError) as e:
            print("token expired")
            return redirect(url_for("auth.four_o_four"))

    else:
        # render the token does not exist error page
        print("does not exist")
        return redirect(url_for("auth.four_o_four"))

@auth.route('/404')
def four_o_four():
    return render_template('404.html')

@auth.route('/create_user_password', methods=['GET', 'POST'])
def create_user_password():
    # Recommending use of session.pop('email', None) to avoid logical error 
    user_email = session['email']
    user_idno = session['idno']
    #  include flask form
    form = CreatePasswordForm()

    if request.method == "POST" and form.validate():
        # insert into database
        password = request.form.get("password")
        # check how to initialise user object so that you set_password(password)
        user = User.query.filter_by(email=user_email, id_number=user_idno).first()
        if user:
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            # Then redirect to another page after successfully submitting the form
            flash(_('Password successfully set'))
            return redirect(url_for('auth.login'))
        else:
            print('user not found')
    return render_template("auth/create_password.html", create_form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid email or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.vote')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('auth.index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             print("Invalid email or password")
#             flash(_('Invalid email or password'))
#             return redirect(url_for('auth.login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('main.index')
#         return redirect(next_page)
#     return render_template('auth/login.html', title=_('Sign In'), form=form)
@auth.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    message='Vote page'
    return render_template('auth/vote.html', message=message)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
