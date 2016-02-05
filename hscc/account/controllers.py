from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for

from flask_login import current_user
from flask_login import login_required

from hscc import db
from hscc import flash_form_errors

from hscc.models import School
from hscc.models import Team
from hscc.models import User

from hscc.account.forms import CreateTeamForm
from hscc.account.forms import EditAccountForm
from hscc.account.forms import JoinTeamForm


mod_account = Blueprint('account', __name__, url_prefix='/account')

@mod_account.route('/', methods=['GET'])
@mod_account.route('/home', methods=['GET'])
@mod_account.route('/home/', methods=['GET'])
@login_required
def home():
    """Return the account home page"""
    return render_template('account/home.html')

@mod_account.route('/edit', methods=['GET', 'POST'])
@mod_account.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    """Return the account edit page"""
    form = EditAccountForm()

    if form.validate_on_submit():
        db.session.commit()
        flash('Your changes have been saved successfully', 'alert-success')
        return redirect(url_for('account.home'))
    else:
        flash_form_errors(form)
        form.grade.data = current_user.grade
        form.shirt_size.data = current_user.shirt_size
        if current_user.language:
            language = current_user.language.name
        if current_user.allergies:
            form.allergies_text.data = current_user.allergies.text
        return render_template('account/edit.html', form=form, lang=language)


@mod_account.route('/my_school', methods=['GET'])
@mod_account.route('/my_school/', methods=['GET'])
def my_school():
    """Return the user's own school details"""
    if current_user.school.id:
        return redirect(url_for('account.school', id=current_user.school.id))
    else:
        return redirect(url_for('account.schools'))


@mod_account.route('/school/<int:id>', methods=['GET'])
@mod_account.route('/school/<int:id>/', methods=['GET'])
def school(id):
    """Return the school with id <id>"""
    sc = School.query.get(id)
    if not sc:
        flash('Error: School not found.', 'alert-warning')
        return redirect(url_for('default.home'))
    return render_template('account/school.html', school=sc)


@mod_account.route('/schools', methods=['GET'])
@mod_account.route('/schools/', methods=['GET'])
def schools():
    """Return a list of schools"""
    sc = School.query.all()
    return render_template('account/schools.html', schools=sc)


@mod_account.route('/create_team', methods=['GET', 'POST'])
@mod_account.route('/create_team/', methods=['GET', 'POST'])
def create_team():
    """Create a new team"""
    form = CreateTeamForm()

    if form.validate_on_submit():
        db.session.add(form.team)
        db.session.commit()

        flash('You are now a member of {}'.format(form.team.name), 'alert-success')
        return redirect(url_for('account.my_team'))
    else:
        flash_form_errors(form)
        return render_template('account/create_team.html', form=form)


@mod_account.route('/join_team/<int:id>', methods=['GET', 'POST'])
@mod_account.route('/join_team/<int:id>/', methods=['GET', 'POST'])
def join_team(id):
    """Join the team with the given team id"""
    t = Team.query.get(id)
    if not t:
        flash('Error: Team not found.', 'alert-warning')
        return redirect(url_for('default.home'))

    form = JoinTeamForm()
    form.team_id.data = t.id

    if form.validate_on_submit():
        db.session.commit()
        flash('Congrats! You are now a member of {}!'.format(t.name), 'alert-success')
        return redirect(url_for('account.team', id=t.id))
    else:
        flash_form_errors(form)
        return render_template('account/join_team.html', team=t, form=form)


@mod_account.route('/my_team', methods=['GET'])
@mod_account.route('/my_team/', methods=['GET'])
def my_team():
    """Return the user's own team details"""
    if current_user.team.id:
        return redirect(url_for('account.team', id=current_user.team.id))
    else:
        return redirect(url_for('account.teams'))


@mod_account.route('/team/<int:id>', methods=['GET'])
@mod_account.route('/team/<int:id>/', methods=['GET'])
def team(id):
    """Return the team with id <id>"""
    t = Team.query.get(id)
    if not t:
        flash('Error: Team not found.', 'alert-warning')
        return redirect(url_for('default.home'))
    return render_template('account/team.html', team=t)


@mod_account.route('/teams', methods=['GET'])
@mod_account.route('/teams/', methods=['GET'])
def teams():
    """Return a list of teams from the school with id <school_id>"""
    ts = Team.query.all()
    return render_template('account/teams.html', teams=ts)
