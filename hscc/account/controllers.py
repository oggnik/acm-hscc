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
from hscc.models import User


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
    return render_template('account/edit.html')


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
        # TODO: Error: No school found
        return redirect(url_for('default.home'))
    return render_template('account/school.html', school=sc)


@mod_account.route('/schools', methods=['GET'])
@mod_account.route('/schools/', methods=['GET'])
def schools():
    """Return a list of schools"""
    sc = School.query.all()
    return render_template('account/schools.html', schools=sc)


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
        # TODO: Error: No team found
        return redirect(url_for('default.home'))
    return render_teamplate('account/team.html', team=t)


@mod_account.route('/teams/<int:school_id>', methods=['GET'])
@mod_account.route('/teams/<int:school_id>/', methods=['GET'])
def teams(school_id):
    """Return a list of teams from the school with id <school_id>"""
    ts = Team.query.all()
    return render_template('account/teams.html', teams=ts)
