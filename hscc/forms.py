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
from wtforms import validators

from hscc.models import Grade
from hscc.models import School
from hscc.models import State
from hscc.models import User
from hscc.models import PasswordReset


class RegistrationForm(Form):
    """A form for registering a new user"""

    def __init__(self, *args, **kwargs):
        """Initialize the registration form"""
        Form.__init__(self, *args, **kwargs)
        self.school = None
        self.user = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        if self.school_id.data and self.school_id.data.isdigit():
            self.school = School.query.get(int(self.school_id.data))

        if not self.school:
            self.school = School(
                name=self.school_name.data,
                state=self.school_state.data,
            )

        self.user = User.query.filter_by(email=self.email.data).first()
        if self.user:
            self.email.errors.append('An account with that email address has already registered')
            return False

        self.user = User(
            name=self.name.data,
            email=self.email.data,
            school=self.school,
            partner_email=self.partner_email.data,
            grade=self.grade.data,
            password=self.password.data,
        )

        return True


    # Fields for a RegistrationForm
    name = TextField(
        'Full Name',
        validators=[
            validators.Required(message='You must provide your full name'),
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
        choices=[(st.value, st.name) for st in State],
        validators=[
            validators.Required(message='Please provide your school state'),
        ],
        coerce=int,
    )

    partner_email = TextField(
        'Partner Email',
        validators=[
            validators.Optional(),
        ],
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

    grade = SelectField(
        'Grade',
        choices=[(gr.value, gr.name) for gr in Grade],
        validators=[
            validators.Required(message='Please enter your grade in school'),
        ],
        coerce=int,
    )


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
        # TODO

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
