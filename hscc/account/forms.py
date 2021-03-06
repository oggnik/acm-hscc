"""Forms for acm_hscc

Author: Logan Gore
This file lists all forms for the acm_hscc site
"""

from flask_login import current_user
from flask_wtf import Form

from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import validators

from hscc.models import Allergies
from hscc.models import Grade
from hscc.models import Language
from hscc.models import ShirtSize
from hscc.models import Team


class CreateTeamForm(Form):
    """A form for creating a new team"""

    def __init__(self, *args, **kwargs):
        """Initialize the form"""
        Form.__init__(self, *args, **kwargs)
        self.team = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        # Make sure the team doesn't already exist
        self.team = Team.query.filter(Team.name.ilike(self.team_name.data)).first()
        if self.team:
            self.team_name.errors.append('Sorry, that team name is already registered')
            return False

        self.team = Team.get_or_create(self.team_name.data, current_user.school)
        current_user.team = self.team
        return True

    team_name = TextField(
        'Team Name',
        validators=[
            validators.Required(message='You must provide a team name'),
        ],
    )


class JoinTeamForm(Form):
    """A form for joining a team"""

    def __init__(self, *args, **kwargs):
        """Initialize the form"""
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        if not self.confirm.data:
            self.confirm.errors.append('You must confirm your intentions')
            return False

        new_team = Team.query.get(int(self.team_id.data))
        if not new_team:
            self.team_id.errors.append('Team not found')
            return False

        if current_user.team and new_team.id == current_user.team.id:
            self.team_id.errors.append("You're already a member of this team")
            return False

        if len(new_team.users) == 2:
            self.team_id.errors.append('Oops! That team is already full!')
            return False

        if new_team.school.id != current_user.school.id:
            self.team_id.errors.append("Sorry, you can't join a team from another school")
            return False

        current_user.team = new_team
        return True

    confirm = BooleanField()

    team_id = HiddenField()


class EditAccountForm(Form):
    """A form for editing a user account"""

    def __init__(self, *args, **kwargs):
        """Initialize the form"""
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        if self.allergies_text.data:
            self.allergies = Allergies(text=self.allergies_text.data)
        else:
            self.allergies = Allergies(text='')

        if self.language.data:
            current_user.language = Language.get_or_create(self.language.data)

        current_user.grade = self.grade.data
        current_user.shirt_size = self.shirt_size.data
        current_user.allergies = self.allergies

        return True

    grade = SelectField(
        'Grade',
        choices=[(gr.value[0], gr.value[1]) for gr in Grade],
        coerce=int,
        default=0,
    )

    language = TextField(
        'Preferred Language',
        validators=[],
    )

    shirt_size = SelectField(
        'Shirt Size',
        choices=[(sz.value[0], sz.value[1]) for sz in ShirtSize],
        coerce=int,
        default=0,
    )

    allergies_text = TextAreaField('Food Allergies')
