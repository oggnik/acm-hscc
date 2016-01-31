from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flask_login import login_user
from flask_login import logout_user

from hscc import db
from hscc import flash_form_errors

from hscc.forms import ForgotForm
from hscc.forms import LoginForm
from hscc.forms import NewPasswordForm
from hscc.forms import RegistrationForm

from hscc.models import School
from hscc.models import Team

mod_default = Blueprint('default', __name__)

@mod_default.route('/')
@mod_default.route('/home')
@mod_default.route('/home/')
@mod_default.route('/index')
@mod_default.route('/index.html')
def home():
    """Render the index page for the ACM-HSCC site"""
    return render_template('index.html')

@mod_default.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(os.path.join(app.root_path, 'static'), 'images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@mod_default.route('/contact')
@mod_default.route('/contact.html')
def contact():
    """Render the contact us page for the ACM-HSCC site"""
    return render_template('contact.html')

@mod_default.route('/register', methods=['GET', 'POST'])
@mod_default.route('/register/', methods=['GET', 'POST'])
def register():
    """Render the registration page for the ACM-HSCC site"""
    form = RegistrationForm()

    if form.validate_on_submit():
        db.session.add(form.user)
        db.session.add(form.allergies)
        db.session.commit()

        flash('You have successfully registered for the ACM-HSCC', 'alert-success')
        login_user(form.user)
        return redirect(url_for('default.home'))
    else:
        flash_form_errors(form)
        return render_template('register.html', form=form)


@mod_default.route('/login', methods=['GET', 'POST'])
@mod_default.route('/login/', methods=['GET', 'POST'])
def login():
    """Render the login page for the ACM-HSCC site"""
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.user, remember=form.remember.data)
        flash('You are now logged in to the ACM-HSCC site', 'alert-success')
        return redirect(url_for('default.home'))
    else:
        flash_form_errors(form)
        return render_template('login.html', form=form)


@mod_default.route('/logout', methods=['POST'])
@mod_default.route('/logout/', methods=['POST'])
def logout():
    """Log the user out of their account"""
    logout_user()
    return redirect(url_for('default.home'))


@mod_default.route('/forgot', methods=['GET', 'POST'])
@mod_default.route('/forgot/', methods=['GET', 'POST'])
def forgot():
    """Render the forgot password page for the ACM-HSCC site"""
    form = ForgotForm()

    if form.validate_on_submit():
        db.session.add(form.pw_reset)
        db.session.commit()

        form.pw_reset.send()
        flash('A password reset link has been sent to your email', 'alert-success')
        return redirect(url_for('default.home'))
    else:
        flash_form_errors(form)
        return render_template('forgot.html', form=form)


@mod_default.route('/reset_pass/<key>', methods=['GET', 'POST'])
@mod_default.route('/reset_pass/<key>/', methods=['GET', 'POST'])
def reset_pass(key):
    """Render the reset password page for the ACM-HSCC site"""
    form = NewPasswordForm()

    if form.validate_on_submit():
        form.user.set_password(form.password.data)
        db.session.delete(form.pw_reset)
        db.session.commit()

        flash('Your password has been successfully reset', 'alert-success')
        login_user(form.user)
        return redirect(url_for('default.home'))
    else:
        flash_form_errors(form)
        form.key.data = key
        return render_template('reset_pass.html', form=form)


@mod_default.route('/autocomplete/schools', methods=['GET'])
@mod_default.route('/autocomplete/schools/', methods=['GET'])
def autocomplete_schools():
    """Return a list of schools for the autocomplete field"""
    schools = School.query.all()
    return jsonify(json_list=[school.name for school in schools])


@mod_default.route('/autocomplete/teams', methods=['GET'])
@mod_default.route('/autocomplete/teams/', methods=['GET'])
def autocomplete_teams():
    """Return a list of schools for the autocomplete field"""
    school_name = request.args.get('school_name')
    school = School.query.filter(School.name.ilike(school_name)).first()
    if not school:
        return jsonify(**{})

    return jsonify(json_list=[t.name for t in school.teams])
