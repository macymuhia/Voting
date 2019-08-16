from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, IntegerField
from wtforms.validators import Required, EqualTo, Email


class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    surname = StringField('Surname', validators=[Required()])
    id_number = IntegerField('ID Number', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    county = StringField('County', validators=[Required()])
    submit = SubmitField('Submit')

