from flask import render_template, request,redirect, url_for
import datetime
import os
import jwt
from . import main
from .forms import UserRegistrationForm
from .. import db
from ..email import mail_message
from ..utils import token_url
from ..models import User

# views
@main.route("/register_user", methods=['GET', 'POST'])
def register_user():
    reg_form =  UserRegistrationForm()

    if reg_form.validate_on_submit():

        user = User(
            first_name=reg_form.first_name.data, 
            last_name=reg_form.last_name.data, 
            surname=reg_form.surname.data,
            id_number=reg_form.id_number.data,
            email=reg_form.email.data,
            county=reg_form.county.data
            )
        db.session.add(user)
        db.session.commit()

        return render_template('user-registration.html', registration_form=reg_form)
    return render_template('user-registration.html', registration_form=reg_form)


