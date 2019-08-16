from flask import render_template, request,redirect, url_for
import datetime
import os
import jwt
from . import auth
from .forms import CreatePasswordForm, SendEmailsForm
from ..email import mail_message
from ..utils import token_url
from ..models import User

# views
@auth.route("/", methods=['GET', 'POST'])
def index():
    send_email_form = SendEmailsForm()
    users = User.query.all()
    # To get user from DB and get email to send emails to

    current_user_name ='' 
    expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    for user in users:
        create_pwd_url = token_url(user.id, user.email, expiry)
        current_user_name =  user.first_name
        print(create_pwd_url)
        mail_message('iVote', 'email/welcome_user', user.email, url=create_pwd_url)
    print(current_user_name)
    return render_template('index.html', send_email_form=send_email_form, user=current_user_name, url=create_pwd_url)


@auth.route("/create_password", methods=['GET', 'POST'])
def create_password():
    
    if 'token' in request.args:
        # Token exist, etxract, decode an redirect to the create password page
        secret_key = os.environ.get('JWT_SECRET')
        algorithm  = os.environ.get('JWT_ALGORITHM')
        token = request.args.get('token')
        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithm=algorithm
            )
            print(payload['email'])

            email = payload['email']
            idno = payload['id']

            # verify user exist with email and id from the payload
            # reditrect user to create password page
            return redirect(url_for('auth.create_user_password', email = email, id = idno))

        except (jwt.ExpiredSignatureError, jwt.DecodeError) as e:
            print('token expired')
            return redirect(url_for('auth.four_o_four'))

    else:
        # render the token does not exist error page 
        print("does not exist")
        return redirect(url_for('auth.four_o_four'))

@auth.route('/404')
def four_o_four():
    return render_template('404.html')

@auth.route('/create_user_password', methods=['GET', 'POST'])
def create_user_password():
    #  include flask form
    form = CreatePasswordForm()

    if request.method == "POST" and form.validate():
        # insert into database
        password = request.form.get("password")
        print(password)
        # check how to initialise user object so that you set_password(password)
        user = User.objects.get(email = form.email.data)
        user.set_password(password)

        # Then redirect to another page after successfully submitting the form

    return render_template('auth/create_password.html', create_form=form)
