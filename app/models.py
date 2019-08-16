from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    id_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(255), unique=True, index=True)
    county = db.Column(db.String(255))
    # role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'


# class Role(db.Model):
#     __tablename__ = 'roles'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     users = db.relationship('User', backref='role', lazy='dynamic')


# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))
