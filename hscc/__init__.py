import os
import sys

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect

from htmlmin.main import minify

# Define the web app
sys.stdout.write('Creating Flask app...')
sys.stdout.flush()
app = Flask(__name__)
sys.stdout.write('Done\n')

# Load app configuration
sys.stdout.write('Loading app config...')
sys.stdout.flush()
app.config.from_object('config')
sys.stdout.write('Done\n')

# Load SQLAlchemy relationships
sys.stdout.write('Defining SQLAlchemy object relations...')
sys.stdout.flush()
db = SQLAlchemy(app)
sys.stdout.write('Done\n')

# Create the login manager
sys.stdout.write('Creating LoginManager...')
sys.stdout.flush()
login_manager = LoginManager(app)
login_manager.login_view = 'default.login'
sys.stdout.write('Done\n')

# Configure SMTP client
sys.stdout.write('Configuring SMTP service...')
sys.stdout.flush()
mail = Mail(app)
sys.stdout.write('Done\n')

# Enable CSRF protection
sys.stdout.write('Enabling CSRF protection...')
sys.stdout.flush()
csrf = CsrfProtect(app)
sys.stdout.write('Done\n')

# Register error handlers
sys.stdout.write('Registering error handlers...')
sys.stdout.flush()
@app.errorhandler(404)
def not_found(error):
    """Render the default 404 template"""
    return render_template('404.html', error=error), 404

@app.errorhandler(500)
def server_error(error):
    """Render the default 500 template"""
    return render_template('500.html', error=error), 500
sys.stdout.write('Done\n')

# Minify sent HTML text
sys.stdout.write('Loading HTML minifier...')
sys.stdout.flush()
@app.after_request
def response_minify(response):
    """Minify HTML response to reduce bandwidth"""
    if response.content_type == u'text/html; charset=utf-8':
        response.set_data(minify(response.get_data(as_text=True)))
    return response
sys.stdout.write('Done\n')

# Define form error handler
sys.stdout.write('Defining form error handler...')
sys.stdout.flush()
def flash_form_errors(form):
    """Flash form errors to the user"""
    for field, errors in form.errors.items():
        for error in errors:
            flash('%s: %s' % (getattr(form, field).label.text, error), 'alert-danger')
sys.stdout.write('Done\n')

# Import blueprints
sys.stdout.write('Importing blueprints...')
sys.stdout.flush()
from hscc.controllers import mod_default
from hscc.account.controllers import mod_account
from hscc.admin.controllers import mod_admin
sys.stdout.write('Done\n')

# Register blueprints
sys.stdout.write('Registering blueprints...')
sys.stdout.flush()
app.register_blueprint(mod_default)
app.register_blueprint(mod_account)
app.register_blueprint(mod_admin)
sys.stdout.write('Done\n')

# All done!
sys.stdout.write('\nApp done loading.\n')
