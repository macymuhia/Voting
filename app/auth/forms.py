from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, IntegerField, BooleanField
from wtforms.validators import Required, EqualTo, Email

class CreatePasswordForm(FlaskForm):
    password = PasswordField('Create Password', validators=[Required(), EqualTo('confirm_password', message='Password must match')])
    confirm_password = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Submit')


class SendEmailsForm(FlaskForm):
    submit = SubmitField('Send emails')


class LoginForm(FlaskForm):
    username = StringField(('Email'), validators=[Required()])
    password = PasswordField(('Password'), validators=[Required()])
    remember_me = BooleanField(('Remember Me'))
    submit = SubmitField(('Sign In'))
