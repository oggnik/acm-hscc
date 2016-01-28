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
    pass


@mod_account.route('/school/<int:id>', methods=['GET'])
@mod_account.route('/school/<int:id>/', methods=['GET'])
def school(id):
    pass


@mod_account.route('/my_team', methods=['GET'])
@mod_account.route('/my_team/', methods=['GET'])
def my_team():
    pass


@mod_account.route('/team/<int:id>', methods=['GET'])
@mod_account.route('/team/<int:id>/', methods=['GET'])
def team(id):
    pass


@mod_account.route('/teams/<int:school_id>', methods=['GET'])
@mod_account.route('/teams/<int:school_id>/', methods=['GET'])
def teams(school_id):
    pass
