"""Models for acm_hscc

Author: Logan Gore
This file is responsible for defining models for the acm_hscc site
"""

import datetime
import os
import random
import string

from flask_mail import Message
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from hscc import db
from hscc import login_manager
from hscc import mail


@login_manager.user_loader
def user_loader(user_id):
    """Unique user loader for the login manager"""
    return User.query.get(user_id)


class PasswordReset(db.Model):
    """Model for password reset key"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    key = db.Column(db.String(64))
    expiration = db.Column(db.DateTime)

    def __init__(self, user, key=None):
        """Initialize a  model"""
        if not key:
            key = ''.join(
                random.choice(string.ascii_letters + string.digits)
                for _ in range(60)
            )
        self.user = user
        self.key = key
        # Add one additional day so the user can potentially reset their password at midnight
        self.expiration = datetime.datetime.now() + datetime.timedelta(days=8)

    def __repr__(self):
        """Return a descriptive representation of a password reset"""
        return '<Reset password for %r>' % self.user

    def send(self):
        """Send the PasswordReset"""
        title = 'Reset Your ACM-HSCC Password'
        url = '{site}/resetpass/{key}'.format(
            site=os.environ['ACM_HSCC_SITE_URL'],
            key=self.key,
        )
        content = 'Please go to the link: {url}'.format(url=url)

        msg = Message(title, recipients=[self.email])
        msg.body = content
        mail.send(msg)


class User(db.Model):
    """Model representing a basic site user"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    pw_reset = db.relationship(PasswordReset, backref='user')

    def __init__(self, name, email, password, school):
        """Initialize a student model"""
        self.name = name
        self.email = email
        self.school = school
        self.set_password(password)
        self.is_admin = False

    def __repr__(self):
        """Return a descriptive representation of a user"""
        return '<User %s>' % self.name

    @property
    def is_authenticated(self):
        """(Flask-Login) all users are authenticated"""
        return True

    @property
    def is_active(self):
        """(Flask-Login) all users are active"""
        return True

    @property
    def is_anonymous(self):
        """(Flask-Login) all users are NOT anonymous"""
        return False

    def get_id(self):
        """(Flask-Login) retrieve a user's unique id"""
        return self.id

    def set_password(self, new_password):
        """Change the user's password to the new password"""
        self.password = generate_password_hash(new_password)

    def check_password(self, password):
        """Check the user's password against the given value"""
        return check_password_hash(self.password, password)


class School(db.Model):
    """Model representing a high school"""

    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    state = db.Column(db.Integer)
    students = db.relationship(User, backref='school')

    def __init__(self, name, state):
        """Initialize a school model"""
        self.name = name
        self.state = state
        self.students = []

    def __repr__(self):
        """Return a descriptive representation of a school"""
        return '<School %s>' % self.name
