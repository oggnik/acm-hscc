from collections import Counter
from functools import wraps

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for

from flask_login import current_user
from flask_login import login_required

from hscc import db
from hscc import flash_form_errors

from hscc.models import Grade
from hscc.models import Language
from hscc.models import School
from hscc.models import ShirtSize
from hscc.models import State
from hscc.models import User

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(func):
    """Decorator method to check that a route is only accessible by admins"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You must login first', 'alert-danger')
            return redirect(url_for('admin.login'))
        if not current_user.is_admin:
            flash('This page is for administrators only', 'alert-danger')
            return redirect(url_for('admin.home'))
        return func(*args, **kwargs)
    return decorated_function


@mod_admin.route('/schools', methods=['GET', 'POST'])
@mod_admin.route('/schools/', methods=['GET', 'POST'])
@admin_required
def view_schools():
    """View all currently active schools"""
    schools = School.query.all()
    return render_template('admin/schools.html', schools=schools)


@mod_admin.route('/users', methods=['GET', 'POST'])
@mod_admin.route('/users/', methods=['GET', 'POST'])
@mod_admin.route('/users/<int:school_id>', methods=['GET', 'POST'])
@mod_admin.route('/users/<int:school_id>/', methods=['GET', 'POST'])
@admin_required
def view_users(school_id=0):
    """View all currently active users"""
    school = None
    if school_id:
        school = School.query.get(school_id)
        if not school:
            flash('Error: School not found', 'alert-danger')
            return redirect(url_for('admin.home'))
        users = school.students
    else:
        users = User.query.all()
    return render_template('admin/users.html', users=users, school=school)

@mod_admin.route('/summary', methods=['GET'])
@mod_admin.route('/summary/', methods=['GET'])
@admin_required
def summary():
    """View a summary of registration statistics"""
    users = User.query.filter_by(is_admin=False).all()
    languages = Counter(u.language.name for u in users if u.language)
    shirt_sizes = Counter(ShirtSize.get(u.shirt_size) for u in users)
    grades = Counter(Grade.get(u.grade) for u in users)
    states = Counter(State.get(u.school.state) for u in users if u.school)

    return render_template(
        'admin/summary.html',
        users=users,
        languages=languages,
        shirt_sizes=shirt_sizes,
        grades=grades,
        states=states,
    )
