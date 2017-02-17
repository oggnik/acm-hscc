"""Models for acm_hscc

Author: Logan Gore
This file is responsible for defining models for the acm_hscc site
"""

import datetime
import enum
import os
import random
import string

from flask_login import UserMixin
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


class Status(enum.Enum):
    """An enum of user states in terms of being accepted"""
    Applied = (0, 'Applied')
    Accepted = (1, 'Accepted')
    Waitlisted = (2, 'Waitlisted')

    @classmethod
    def get(cls, st):
        """Retrieve the text representation of a State"""
        for status in Status:
            if status.value[0] == st:
                return status.value[1]
        return None

class State(enum.Enum):
    """An enum of states allowed to register in this competition"""
    Indiana = (0, 'Indiana')
    Illinois = (1, 'Illinois')
    Kentucky = (2, 'Kentucky')
    Michigan = (3, 'Michigan')
    Wisconsin = (4, 'Wisconsin')

    @classmethod
    def get(cls, st):
        """Retrieve the text representation of a State"""
        for state in State:
            if state.value[0] == st:
                return state.value[1]
        return None


class Grade(enum.Enum):
    """An enum of grades allowed to register in this competition"""
    Freshman = (0, 'Freshman')
    Sophomore = (1, 'Sophomore')
    Junior = (2, 'Junior')
    Senior = (3, 'Senior')

    @classmethod
    def get(cls, gr):
        """Retrieve the text representation of a Grade"""
        for grade in Grade:
            if grade.value[0] == gr:
                return grade.value[1]
        return None


class ShirtSize(enum.Enum):
    """An enum of T-shirt sizes"""
    XSmall = (0, 'X-Small')
    Small = (1, 'Small')
    Medium = (2, 'Medium')
    Large = (3, 'Large')
    XLarge = (4, 'X-Large')
    XXLarge = (5, '2X-Large')
    XXXLarge = (6, '3X-Large')

    @classmethod
    def get(cls, sz):
        """Retrieve the text representation of a ShirtSize"""
        for shirt_size in ShirtSize:
            if shirt_size.value[0] == sz:
                return shirt_size.value[1]
        return None


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
        self.email = user.email
        self.key = key
        # Add one additional day so the user can potentially reset their password at midnight
        self.expiration = datetime.datetime.now() + datetime.timedelta(days=8)

    def __repr__(self):
        """Return a descriptive representation of a password reset"""
        return '<Reset password for %r>' % self.user

    def send(self):
        """Send the PasswordReset"""
        title = 'Reset Your ACM-HSCC Password'
        url = '{site}/reset_pass/{key}'.format(
            site=os.environ['ACM_HSCC_SITE_URL'],
            key=self.key,
        )
        content = 'Please go to the link: {url}'.format(url=url)

        msg = Message(title, recipients=[self.email])
        msg.body = content
        mail.send(msg)


class Allergies(db.Model):
    """Model representing a student's allergies"""

    __tablename__ = 'allergies'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))


class Language(db.Model):
    """Model representing a programming language"""

    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

    @classmethod
    def get_or_create(cls, name):
        """Retrieve a language or create a new one if the name isn't in use"""
        language = Language.query.filter(Language.name.ilike(name)).first()
        if not language:
            language = Language(name=name)
            db.session.add(language)
            db.session.commit()
        return language


class User(db.Model, UserMixin):
    """Model representing a basic site user"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    allergies_id = db.Column(db.Integer, db.ForeignKey('allergies.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))

    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    grade = db.Column(db.Integer)
    shirt_size = db.Column(db.Integer)
    status = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)

    language = db.relationship(Language)
    allergies = db.relationship(Allergies, backref='user')
    pw_reset = db.relationship(PasswordReset, backref='user')

    def __init__(self, name, email, password, school, team, grade, shirt_size, language, allergies, is_admin=False):
        """Initialize a student model"""
        self.name = name
        self.email = email
        self.set_password(password)
        self.school = school
        self.team = team
        self.grade = grade
        self.shirt_size = shirt_size
        self.language = language
        self.allergies = allergies
        self.status = Status.Applied.value[0]
        self.is_admin = is_admin

    def __repr__(self):
        """Return a descriptive representation of a user"""
        return '<User %s>' % self.name

    def set_password(self, new_password):
        """Change the user's password to the new password"""
        self.password = generate_password_hash(new_password)

    def check_password(self, password):
        """Check the user's password against the given value"""
        return check_password_hash(self.password, password)

    @property
    def grade_name(self):
        """Get the text representation of the student's grade"""
        return Grade.get(self.grade)

    @property
    def shirt_size_name(self):
        """Get the text representation of the student's shirt size"""
        return ShirtSize.get(self.shirt_size)

    @property
    def status_name(self):
        """Get the text representation of the student's application status"""
        return Status.get(self.status)


class Team(db.Model):
    """Model representing a team"""

    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    users = db.relationship(User, backref='team')

    def __init__(self, name, school):
        """Initialize a team model"""
        self.name = name
        self.school = school
        self.users = []

    def __repr__(self):
        """Return a descriptive representation of a user"""
        return '<Team %s>' % self.name

    @classmethod
    def get_or_create(cls, name, school):
        """Retrieve a team or create a new one if the name isn't in use"""
        team = Team.query.filter(Team.name.ilike(name)).first()
        if not team:
            team = Team(name, school)
            db.session.add(team)
            db.session.commit()
        return team


class School(db.Model):
    """Model representing a high school"""

    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    state = db.Column(db.Integer)
    students = db.relationship(User, backref='school')
    teams = db.relationship(Team, backref='school')

    def __init__(self, name, state):
        """Initialize a school model"""
        self.name = name
        self.state = state
        self.students = []
        self.teams = []

    def __repr__(self):
        """Return a descriptive representation of a school"""
        return '<School %s>' % self.name

    @property
    def state_name(self):
        """Get the text representation of the school's state"""
        return State.get(self.state)

    @classmethod
    def get_or_create(cls, name, state):
        """Retrieve a school or create a new one if it hasn't been added yet"""
        school = School.query.filter(School.name.ilike(name)).filter(
            School.state == state
        ).first()
        if not school:
            school = School(name, state)
            db.session.add(school)
            db.session.commit()
        return school
