"""Forms for acm_hscc

Author: Logan Gore
This file lists all forms for the acm_hscc site
"""

from flask_wtf import Form

from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import validators

from hscc.models import Allergies
from hscc.models import Grade
from hscc.models import Language
from hscc.models import School
from hscc.models import ShirtSize
from hscc.models import State
from hscc.models import Team
from hscc.models import User
from hscc.models import PasswordReset


class RegistrationForm(Form):
    """A form for registering a new user"""

    def __init__(self, *args, **kwargs):
        """Initialize the registration form"""
        Form.__init__(self, *args, **kwargs)
        self.user = None
        self.allergies = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        school = None
        if self.school_id.data and self.school_id.data.isdigit():
            school = School.query.get(int(self.school_id.data))

        if not school:
            school = School.get_or_create(
                name=self.school_name.data.upper(),
                state=self.school_state.data,
            )

        self.user = User.query.filter_by(email=self.email.data).first()
        if self.user:
            self.email.errors.append('An account with that email address has already registered')
            return False

        if self.allergies_text.data:
            self.allergies = Allergies(text=self.allergies_text.data)
        else:
            self.allergies = Allergies(text='')

        language = Language.get_or_create(self.language.data)

        team = Team.get_or_create(self.team_name.data, school)
        if team.school.id != school.id:
            self.team_name.errors.append('Sorry, that team name is already registered at another school')
            return False
        elif len(team.users) == 2:
            self.team_name.errors.append('Sorry, that team is already full (limit of 2 students per team)')
            return False

        self.user = User(
            name=self.first_name.data + ' ' + self.last_name.data,
            email=self.email.data,
            password=self.password.data,
            grade=self.grade.data,
            shirt_size=self.shirt_size.data,
            language=language,
            allergies=self.allergies,
            school=school,
            team=team,
        )

        return True


    # Fields for a RegistrationForm
    first_name = TextField(
        'First Name',
        validators=[
            validators.Required(message='You must provide your first name'),
        ],
    )

    last_name = TextField(
        'Last Name',
        validators=[
            validators.Required(message='You must provide your last name'),
        ],
    )

    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(message='You must provide your email address'),
            validators.EqualTo('confirm_email', message='Emails must match')
        ],
    )

    confirm_email = TextField(
        'Confirm Email',
        validators=[
            validators.Email(),
            validators.Required(message='Please confirm your email'),
        ],
    )

    school_id = HiddenField()

    school_name = TextField(
        'School Name',
        validators=[
            validators.Required(message='Please provide your school name'),
        ],
    )

    school_state = SelectField(
        'School State',
        choices=[(st.value[0], st.value[1]) for st in State],
        coerce=int,
        default=0,
    )

    password = PasswordField(
        'Password',
        validators=[
            validators.Required(message='Please enter a password'),
            validators.EqualTo('confirm_password', message='Passwords must match'),
        ],
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            validators.Required(message='Please confirm your password'),
        ],
    )

    team_name = TextField(
        'Team Name',
        validators=[
            validators.Required(message='Please provide your team name'),
        ],
    )

    grade = SelectField(
        'Grade',
        choices=[(gr.value[0], gr.value[1]) for gr in Grade],
        coerce=int,
        default=0,
    )

    shirt_size = SelectField(
        'Shirt Size',
        choices=[(sz.value[0], sz.value[1]) for sz in ShirtSize],
        coerce=int,
        default=0,
    )

    language = TextField(
        'Preferred Programming Language',
        validators=[],
    )

    allergies_text = TextAreaField('Allergies or Health Concerns')


class LoginForm(Form):
    """A form for logging in a user"""

    def __init__(self, *args, **kwargs):
        """Initialize the registration form"""
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        self.user = User.query.filter_by(email=self.email.data).first()
        if not self.user:
            self.email.errors.append('No account with that email found')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Incorrect password')
            return False

        return True


    # Fields for a LoginForm
    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(message='You must provide your email address'),
        ],
    )

    password = PasswordField(
        'Password',
        validators=[
            validators.Required(message='Please enter your password'),
        ],
    )

    remember = BooleanField('Remember me?')


class ForgotForm(Form):
    """A form for recovering an account with a forgotten password"""

    def __init__(self, *args, **kwargs):
        """Initialize the registration form"""
        Form.__init__(self, *args, **kwargs)
        self.pw_reset = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('No account with that email found')
            return False

        self.pw_reset = PasswordReset(user=user)

        return True


    # Fields for a ForgotForm
    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(message='You must provide your email address'),
        ],
    )


class NewPasswordForm(Form):
    """A form for resetting a user's password"""

    def __init__(self, *args, **kwargs):
        """Initialize the registration form"""
        Form.__init__(self, *args, **kwargs)
        self.pw_reset = None
        self.user = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        self.pw_reset = PasswordReset.query.filter_by(key=self.key.data).first()
        if not self.pw_reset:
            self.key.errors.append('Invalid password reset key')
            return False

        self.user = self.pw_reset.user

        return True


    # Fields for a NewPasswordForm
    key = HiddenField()

    password = PasswordField(
        'New Password',
        validators=[
            validators.Required(message='Please enter a password'),
            validators.EqualTo('confirm_password', message='Passwords must match'),
        ],
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            validators.Required(message='Please confirm your password'),
        ],
    )
