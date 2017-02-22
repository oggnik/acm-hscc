import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Dev environment
DEBUG = bool(os.environ['ACM_HSCC_DEBUG'])

# Database setup
SQLALCHEMY_DATABASE_URI = (
    'mysql://{user}:{password}@{host}:{port}/{database}'.format(
        user=os.environ['ACM_HSCC_DB_USERNAME'],
        password=os.environ['ACM_HSCC_DB_PASSWORD'],
        host=os.environ['ACM_HSCC_DB_HOST'],
        port=os.environ['ACM_HSCC_DB_PORT'],
        database=os.environ['ACM_HSCC_DB_NAME'],
    )
)
DATABASE_CONNECT_OPTIONS = {}

# Flask-Mail setup
MAIL_SERVER = os.environ['ACM_HSCC_MAIL_SERVER']
MAIL_PORT = os.environ['ACM_HSCC_MAIL_PORT']
MAIL_USERNAME = os.environ['ACM_HSCC_MAIL_USERNAME']
MAIL_PASSWORD = os.environ['ACM_HSCC_MAIL_PASSWORD']
MAIL_DEFAULT_SENDER = os.environ['ACM_HSCC_MAIL_DEFAULT_SENDER']
MAIL_USE_TLS = bool(os.environ['ACM_HSCC_MAIL_USE_TLS'])
MAIL_USE_SSL = bool(os.environ['ACM_HSCC_MAIL_USE_SSL'])

# Application threads to handle requests
THREADS_PER_PAGE = int(os.environ['ACM_HSCC_THREADS_PER_PAGE'])

# CSRF protection
CSRF_ENABLED = True
CSRF_SESSION_KEY = os.environ['ACM_HSCC_CSRF_SESSION_KEY']
SECRET_KEY = os.environ['ACM_HSCC_SECRET_KEY']

# Basic app configuration
SERVER_HOST = os.environ['ACM_HSCC_SERVER_HOST']
SERVER_PORT = int(os.environ['ACM_HSCC_SERVER_PORT'])